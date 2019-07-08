from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Work Order")
	dataent.db.sql("""update `tabWork Order` set material_transferred_for_manufacturing=
		(select sum(fg_completed_qty) from `tabStock Entry`
			where docstatus=1
			and work_order=`tabWork Order`.name
			and purpose = "Material Transfer for Manufacture")""")
