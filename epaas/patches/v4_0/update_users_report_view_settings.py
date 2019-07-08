# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

from dataent.model.utils.rename_field import update_users_report_view_settings
from epaas.patches.v4_0.fields_to_be_renamed import rename_map

def execute():
	for dt, field_list in rename_map.items():
		for field in field_list:
			update_users_report_view_settings(dt, field[0], field[1])
