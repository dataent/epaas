from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Sales Order")
	dataent.reload_doctype("Sales Order Item")

	if "final_delivery_date" in dataent.db.get_table_columns("Sales Order"):
		dataent.db.sql("""
			update `tabSales Order`
			set delivery_date = final_delivery_date
			where (delivery_date is null or delivery_date = '0000-00-00')
				and order_type = 'Sales'""")

	dataent.db.sql("""
		update `tabSales Order` so, `tabSales Order Item` so_item
		set so_item.delivery_date = so.delivery_date
		where so.name = so_item.parent
			and so.order_type = 'Sales'
			and (so_item.delivery_date is null or so_item.delivery_date = '0000-00-00')
			and (so.delivery_date is not null and so.delivery_date != '0000-00-00')
	""")