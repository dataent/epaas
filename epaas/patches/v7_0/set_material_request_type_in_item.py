from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Item")
	if "default_bom" in dataent.db.get_table_columns("Item"):
		dataent.db.sql("""update `tabItem` 
			set default_material_request_type = (
				case 
					when (default_bom is not null and default_bom != '')
					then 'Manufacture' 
					else 'Purchase' 
				end )""")
				
	else:
		dataent.db.sql("update tabItem set default_material_request_type='Purchase'")