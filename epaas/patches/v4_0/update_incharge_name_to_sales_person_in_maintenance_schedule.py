# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc("support", "doctype", "schedules")
	dataent.reload_doc("support", "doctype", "maintenance_schedule_item")
	
	dataent.db.sql("""update `tabMaintenance Schedule Detail` set sales_person=incharge_name""")
	dataent.db.sql("""update `tabMaintenance Schedule Item` set sales_person=incharge_name""")