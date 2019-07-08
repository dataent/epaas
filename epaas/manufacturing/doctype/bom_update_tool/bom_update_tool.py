# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent, json
from dataent.utils import cstr, flt
from dataent import _
from six import string_types
from epaas.manufacturing.doctype.bom.bom import get_boms_in_bottom_up_order
from dataent.model.document import Document

class BOMUpdateTool(Document):
	def replace_bom(self):
		self.validate_bom()
		self.update_new_bom()
		bom_list = self.get_parent_boms(self.new_bom)
		updated_bom = []

		for bom in bom_list:
			try:
				bom_obj = dataent.get_doc("BOM", bom)
				bom_obj.get_doc_before_save()
				updated_bom = bom_obj.update_cost_and_exploded_items(updated_bom)
				bom_obj.calculate_cost()
				bom_obj.update_parent_cost()
				bom_obj.db_update()
				if (getattr(bom_obj.meta, 'track_changes', False)
					and bom_obj._doc_before_save and not bom_obj.flags.ignore_version):
					bom_obj.save_version()

				dataent.db.commit()
			except Exception:
				dataent.db.rollback()
				dataent.log_error(dataent.get_traceback())

	def validate_bom(self):
		if cstr(self.current_bom) == cstr(self.new_bom):
			dataent.throw(_("Current BOM and New BOM can not be same"))
			
		if dataent.db.get_value("BOM", self.current_bom, "item") \
			!= dataent.db.get_value("BOM", self.new_bom, "item"):
				dataent.throw(_("The selected BOMs are not for the same item"))

	def update_new_bom(self):
		new_bom_unitcost = dataent.db.sql("""select total_cost/quantity
			from `tabBOM` where name = %s""", self.new_bom)
		new_bom_unitcost = flt(new_bom_unitcost[0][0]) if new_bom_unitcost else 0

		dataent.db.sql("""update `tabBOM Item` set bom_no=%s,
			rate=%s, amount=stock_qty*%s where bom_no = %s and docstatus < 2 and parenttype='BOM'""",
			(self.new_bom, new_bom_unitcost, new_bom_unitcost, self.current_bom))

	def get_parent_boms(self, bom, bom_list=None):
		if not bom_list:
			bom_list = []

		data = dataent.db.sql(""" select distinct parent from `tabBOM Item`
			where ifnull(bom_no, '') = %s and docstatus < 2 and parenttype='BOM'""", bom)

		for d in data:
			bom_list.append(d[0])
			self.get_parent_boms(d[0], bom_list)

		return list(set(bom_list))

@dataent.whitelist()
def enqueue_replace_bom(args):
	if isinstance(args, string_types):
		args = json.loads(args)

	dataent.enqueue("epaas.manufacturing.doctype.bom_update_tool.bom_update_tool.replace_bom", args=args, timeout=4000)
	dataent.msgprint(_("Queued for replacing the BOM. It may take a few minutes."))

@dataent.whitelist()
def enqueue_update_cost():
	dataent.enqueue("epaas.manufacturing.doctype.bom_update_tool.bom_update_tool.update_cost")
	dataent.msgprint(_("Queued for updating latest price in all Bill of Materials. It may take a few minutes."))

def update_latest_price_in_all_boms():
	if dataent.db.get_single_value("Manufacturing Settings", "update_bom_costs_automatically"):
		update_cost()

def replace_bom(args):
	args = dataent._dict(args)

	doc = dataent.get_doc("BOM Update Tool")
	doc.current_bom = args.current_bom
	doc.new_bom = args.new_bom
	doc.replace_bom()

def update_cost():
	bom_list = get_boms_in_bottom_up_order()
	for bom in bom_list:
		dataent.get_doc("BOM", bom).update_cost(update_parent=False, from_child_bom=True)