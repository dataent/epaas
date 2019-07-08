from __future__ import unicode_literals
import dataent

def execute():
	if dataent.db.table_exists("Offer Letter") and not dataent.db.table_exists("Job Offer"):
		dataent.rename_doc("DocType", "Offer Letter", "Job Offer", force=True)
		dataent.rename_doc("DocType", "Offer Letter Term", "Job Offer Term", force=True)
		dataent.reload_doc("hr", "doctype", "job_offer")
		dataent.reload_doc("hr", "doctype", "job_offer_term")
		dataent.delete_doc("Print Format", "Offer Letter")