# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.rename_doc import rename_doc

def execute():
	if dataent.db.table_exists("Asset Adjustment") and not dataent.db.table_exists("Asset Value Adjustment"):
		rename_doc('DocType', 'Asset Adjustment', 'Asset Value Adjustment', force=True)
		dataent.reload_doc('assets', 'doctype', 'asset_value_adjustment')