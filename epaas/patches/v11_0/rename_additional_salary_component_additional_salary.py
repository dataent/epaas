from __future__ import unicode_literals
import dataent

# this patch should have been included with this PR https://github.com/dataent/epaas/pull/14302

def execute():
	if dataent.db.table_exists("Additional Salary Component"):
		if not dataent.db.table_exists("Additional Salary"):
			dataent.rename_doc("DocType", "Additional Salary Component", "Additional Salary")

		dataent.delete_doc('DocType', "Additional Salary Component")
