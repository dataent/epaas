from __future__ import unicode_literals
import dataent
from dataent.patches.v6_19.comment_feed_communication import update_timeline_doc_for

def execute():
	for doctype in ("Customer", "Supplier", "Employee", "Project"):
		update_timeline_doc_for(doctype)
