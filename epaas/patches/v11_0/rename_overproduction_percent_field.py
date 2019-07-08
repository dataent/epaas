# Copyright (c) 2018, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from dataent.model.utils.rename_field import rename_field
import dataent

def execute():
	dataent.reload_doc('manufacturing', 'doctype', 'manufacturing_settings')
	rename_field('Manufacturing Settings', 'over_production_allowance_percentage', 'overproduction_percentage_for_sales_order')