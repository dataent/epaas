# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors

from __future__ import unicode_literals
import dataent

def execute():
	dataent.db.set_value("DocType", "Maintenance Schedule", "module", "Maintenance")
	dataent.db.set_value("DocType", "Maintenance Schedule Detail", "module", "Maintenance")
	dataent.db.set_value("DocType", "Maintenance Schedule Item", "module", "Maintenance")
	dataent.db.set_value("DocType", "Maintenance Visit", "module", "Maintenance")
	dataent.db.set_value("DocType", "Maintenance Visit Purpose", "module", "Maintenance")