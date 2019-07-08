from __future__ import unicode_literals
import dataent
from epaas.setup.install import create_default_success_action

def execute():
	dataent.reload_doc("core", "doctype", "success_action")
	create_default_success_action()
