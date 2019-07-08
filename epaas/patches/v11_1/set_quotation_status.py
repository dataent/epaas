from __future__ import unicode_literals
import dataent

def execute():

	dataent.db.sql(""" UPDATE `tabQuotation` set status = 'Open'
		where docstatus = 1 and status = 'Submitted' """)
