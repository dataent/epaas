# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.exists("DocType", "Salary Component"):
		for dt in ("Salary Structure Earning", "Salary Structure Deduction", "Salary Slip Earning", 
			"Salary Slip Deduction", "Earning Type", "Deduction Type"):
				dataent.delete_doc("DocType", dt)
				
					
		for d in dataent.db.sql("""select name from `tabCustom Field` 
			where dt in ('Salary Detail', 'Salary Component')"""):
				dataent.get_doc("Custom Field", d[0]).save()