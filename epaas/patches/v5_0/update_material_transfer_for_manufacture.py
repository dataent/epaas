from __future__ import unicode_literals
import dataent

def execute():
	dataent.db.sql("""update `tabStock Entry` set purpose='Material Transfer for Manufacture'
		where ifnull(work_order, '')!='' and purpose='Material Transfer'""")
