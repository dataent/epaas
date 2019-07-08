from __future__ import unicode_literals
import dataent
from dataent.utils.nestedset import rebuild_tree

def execute():
	dataent.reload_doc("setup", "doctype", "company")
	rebuild_tree('Company', 'parent_company')
