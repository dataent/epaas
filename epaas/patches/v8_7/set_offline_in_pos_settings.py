# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('accounts', 'doctype', 'pos_settings')

	doc = dataent.get_doc('POS Settings')
	doc.use_pos_in_offline_mode = 1
	doc.save()