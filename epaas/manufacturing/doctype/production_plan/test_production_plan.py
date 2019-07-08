# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest
from dataent.utils import nowdate, now_datetime, flt
from epaas.stock.doctype.item.test_item import create_item
from epaas.manufacturing.doctype.production_plan.production_plan import get_sales_orders
from epaas.stock.doctype.stock_reconciliation.test_stock_reconciliation import create_stock_reconciliation
from epaas.selling.doctype.sales_order.test_sales_order import make_sales_order
from epaas.manufacturing.doctype.production_plan.production_plan import get_items_for_material_requests

class TestProductionPlan(unittest.TestCase):
	def setUp(self):
		for item in ['Test Production Item 1', 'Subassembly Item 1',
			'Raw Material Item 1', 'Raw Material Item 2']:
			create_item(item, valuation_rate=100)

			sr = dataent.db.get_value('Stock Reconciliation Item',
				{'item_code': item, 'docstatus': 1}, 'parent')
			if sr:
				sr_doc = dataent.get_doc('Stock Reconciliation', sr)
				sr_doc.cancel()

		create_item('Test Non Stock Raw Material', is_stock_item=0)
		for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'],
			'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1',
			'Test Non Stock Raw Material']}.items():
			if not dataent.db.get_value('BOM', {'item': item}):
				make_bom(item = item, raw_materials = raw_materials)

	def test_production_plan(self):
		pln = create_production_plan(item_code='Test Production Item 1')
		self.assertTrue(len(pln.mr_items), 2)
		pln.make_material_request()

		pln = dataent.get_doc('Production Plan', pln.name)
		self.assertTrue(pln.status, 'Material Requested')
		material_requests = dataent.get_all('Material Request Item', fields = ['distinct parent'],
			filters = {'production_plan': pln.name}, as_list=1)

		self.assertTrue(len(material_requests), 2)

		pln.make_work_order()
		work_orders = dataent.get_all('Work Order', fields = ['name'],
			filters = {'production_plan': pln.name}, as_list=1)

		self.assertTrue(len(work_orders), len(pln.po_items))

		for name in material_requests:
			mr = dataent.get_doc('Material Request', name[0])
			mr.cancel()

		for name in work_orders:
			mr = dataent.delete_doc('Work Order', name[0])

		pln = dataent.get_doc('Production Plan', pln.name)
		pln.cancel()

	def test_production_plan_for_existing_ordered_qty(self):
		sr1 = create_stock_reconciliation(item_code="Raw Material Item 1",
			target="_Test Warehouse - _TC", qty=1, rate=100)
		sr2 = create_stock_reconciliation(item_code="Raw Material Item 2",
			target="_Test Warehouse - _TC", qty=1, rate=100)

		pln = create_production_plan(item_code='Test Production Item 1', ignore_existing_ordered_qty=0)
		self.assertTrue(len(pln.mr_items), 1)
		self.assertTrue(flt(pln.mr_items[0].quantity), 1.0)

		sr1.cancel()
		sr2.cancel()
		pln.cancel()

	def test_production_plan_with_non_stock_item(self):
		pln = create_production_plan(item_code='Test Production Item 1', include_non_stock_items=0)
		self.assertTrue(len(pln.mr_items), 3)
		pln.cancel()

	def test_production_plan_without_multi_level(self):
		pln = create_production_plan(item_code='Test Production Item 1', use_multi_level_bom=0)
		self.assertTrue(len(pln.mr_items), 2)
		pln.cancel()

	def test_production_plan_without_multi_level_for_existing_ordered_qty(self):
		sr1 = create_stock_reconciliation(item_code="Raw Material Item 1",
			target="_Test Warehouse - _TC", qty=1, rate=100)
		sr2 = create_stock_reconciliation(item_code="Subassembly Item 1",
			target="_Test Warehouse - _TC", qty=1, rate=100)

		pln = create_production_plan(item_code='Test Production Item 1',
			use_multi_level_bom=0, ignore_existing_ordered_qty=0)
		self.assertTrue(len(pln.mr_items), 0)

		sr1.cancel()
		sr2.cancel()
		pln.cancel()

	def test_production_plan_sales_orders(self):
		item = 'Test Production Item 1'
		so = make_sales_order(item_code=item, qty=5)
		sales_order = so.name
		sales_order_item = so.items[0].name

		pln = dataent.new_doc('Production Plan')
		pln.company = so.company
		pln.get_items_from = 'Sales Order'

		pln.append('sales_orders', {
			'sales_order': so.name,
			'sales_order_date': so.transaction_date,
			'customer': so.customer,
			'grand_total': so.grand_total
		})

		pln.get_so_items()
		pln.submit()
		pln.make_work_order()

		work_order = dataent.db.get_value('Work Order', {'sales_order': sales_order,
			'production_plan': pln.name, 'sales_order_item': sales_order_item}, 'name')

		wo_doc = dataent.get_doc('Work Order', work_order)
		wo_doc.update({
			'wip_warehouse': '_Test Warehouse 1 - _TC',
			'fg_warehouse': '_Test Warehouse - _TC'
		})
		wo_doc.submit()

		so_wo_qty = dataent.db.get_value('Sales Order Item', sales_order_item, 'work_order_qty')
		self.assertTrue(so_wo_qty, 5)

		pln = dataent.new_doc('Production Plan')
		pln.update({
			'from_date': so.transaction_date,
			'to_date': so.transaction_date,
			'customer': so.customer,
			'item_code': item
		})
		sales_orders = get_sales_orders(pln) or {}
		sales_orders = [d.get('name') for d in sales_orders if d.get('name') == sales_order]

		self.assertEqual(sales_orders, [])

def create_production_plan(**args):
	args = dataent._dict(args)

	pln = dataent.get_doc({
		'doctype': 'Production Plan',
		'company': args.company or '_Test Company',
		'posting_date': nowdate(),
		'include_non_stock_items': args.include_non_stock_items or 1,
		'include_subcontracted_items': args.include_subcontracted_items or 1,
		'ignore_existing_ordered_qty': args.ignore_existing_ordered_qty or 1,
		'po_items': [{
			'use_multi_level_bom': args.use_multi_level_bom or 1,
			'item_code': args.item_code,
			'bom_no': dataent.db.get_value('Item', args.item_code, 'default_bom'),
			'planned_qty': args.planned_qty or 1,
			'planned_start_date': args.planned_start_date or now_datetime()
		}]
	})
	mr_items = get_items_for_material_requests(pln.as_dict())
	for d in mr_items:
		pln.append('mr_items', d)

	if not args.do_not_save:
		pln.insert()
		if not args.do_not_submit:
			pln.submit()

	return pln

def make_bom(**args):
	args = dataent._dict(args)

	bom = dataent.get_doc({
		'doctype': "BOM",
		'is_default': 1,
		'item': args.item,
		'quantity': args.quantity or 1,
		'company': args.company or '_Test Company'
	})

	for item in args.raw_materials:
		item_doc = dataent.get_doc('Item', item)

		bom.append('items', {
			'item_code': item,
			'qty': 1,
			'uom': item_doc.stock_uom,
			'stock_uom': item_doc.stock_uom,
			'rate': item_doc.valuation_rate or args.rate,
		})

	bom.insert(ignore_permissions=True)
	bom.submit()