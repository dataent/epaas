# Copyright (c) 2013, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()

	data = get_bom_stock(filters)

	return columns, data

def get_columns():
	"""return columns"""
	columns = [
		_("Item") + ":Link/Item:150",
		_("Description") + "::500",
		_("Qty per BOM Line") + ":Float:100",
		_("Required Qty") + ":Float:100",
		_("In Stock Qty") + ":Float:100",
		_("Enough Parts to Build") + ":Float:200",
	]

	return columns

def get_bom_stock(filters):
	conditions = ""
	bom = filters.get("bom")

	table = "`tabBOM Item`"
	qty_field = "qty"

	qty_to_produce = filters.get("qty_to_produce", 1)
	if  int(qty_to_produce) <= 0:
		dataent.throw(_("Quantity to Produce can not be less than Zero"))

	if filters.get("show_exploded_view"):
		table = "`tabBOM Explosion Item`"
		qty_field = "stock_qty"

	if filters.get("warehouse"):
		warehouse_details = dataent.db.get_value("Warehouse", filters.get("warehouse"), ["lft", "rgt"], as_dict=1)
		if warehouse_details:
			conditions += " and exists (select name from `tabWarehouse` wh \
				where wh.lft >= %s and wh.rgt <= %s and ledger.warehouse = wh.name)" % (warehouse_details.lft,
				warehouse_details.rgt)
		else:
			conditions += " and ledger.warehouse = '%s'" % dataent.db.escape(filters.get("warehouse"))

	else:
		conditions += ""

	return dataent.db.sql("""
			SELECT
				bom_item.item_code,
				bom_item.description ,
				bom_item.{qty_field},
				bom_item.{qty_field} * {qty_to_produce},
				sum(ledger.actual_qty) as actual_qty,
				sum(FLOOR(ledger.actual_qty / (bom_item.{qty_field} * {qty_to_produce})))
			FROM
				{table} AS bom_item
				LEFT JOIN `tabBin` AS ledger
				ON bom_item.item_code = ledger.item_code
				{conditions}
			WHERE
				bom_item.parent = '{bom}' and bom_item.parenttype='BOM'

			GROUP BY bom_item.item_code""".format(
				qty_field=qty_field,
				table=table,
				conditions=conditions,
				bom=bom,
				qty_to_produce=qty_to_produce or 1)
			)
