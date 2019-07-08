# Copyright (c) 2016, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.utils import cstr

def execute():
	dataent.reload_doc("stock", "doctype", "manufacturer")
	dataent.reload_doctype("Item")
	
	for d in dataent.db.sql("""select distinct manufacturer from tabItem 
		where ifnull(manufacturer, '') != '' and disabled=0"""):
			manufacturer_name = cstr(d[0]).strip()
			if manufacturer_name and not dataent.db.exists("Manufacturer", manufacturer_name):
				man = dataent.new_doc("Manufacturer")
				man.short_name = manufacturer_name
				man.full_name = manufacturer_name
				man.save()
