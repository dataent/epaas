from __future__ import unicode_literals
import dataent

def execute():
	company = dataent.get_all('Company', filters = {'country': 'India'})
	if not company:
		if dataent.db.exists("DocType", "GST Settings"):
			dataent.delete_doc("DocType", "GST Settings")
			dataent.delete_doc("DocType", "GST HSN Code")
		
			for report_name in ('GST Sales Register', 'GST Purchase Register',
				'GST Itemised Sales Register', 'GST Itemised Purchase Register'):

				dataent.delete_doc('Report', report_name)