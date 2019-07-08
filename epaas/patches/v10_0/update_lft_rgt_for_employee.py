from __future__ import unicode_literals
import dataent
from dataent.utils.nestedset import rebuild_tree

def execute():
    """ assign lft and rgt appropriately """
    dataent.reload_doc("hr", "doctype", "employee")

    rebuild_tree("Employee", "reports_to")