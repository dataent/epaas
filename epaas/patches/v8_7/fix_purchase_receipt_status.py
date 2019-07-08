from __future__ import unicode_literals
import dataent

def execute():
	# there is no more status called "Submitted", there was an old issue that used
	# to set it as Submitted, fixed in this commit
	dataent.db.sql("""
	update
		`tabPurchase Receipt`
	set
		status = 'To Bill'
	where
		status = 'Submitted'""")