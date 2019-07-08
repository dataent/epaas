# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

from epaas.buying.doctype.supplier_scorecard.supplier_scorecard import make_default_records
def execute():
	dataent.reload_doc('buying', 'doctype', 'supplier_scorecard_variable')
	dataent.reload_doc('buying', 'doctype', 'supplier_scorecard_standing')
	make_default_records()