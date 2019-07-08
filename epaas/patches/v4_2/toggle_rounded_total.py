# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	global_defaults = dataent.get_doc("Global Defaults", "Global Defaults")
	global_defaults.toggle_rounded_total()
