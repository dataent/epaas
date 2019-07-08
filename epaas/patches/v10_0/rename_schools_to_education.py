# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	# rename the School module as Education

	# rename the school module
	if dataent.db.exists('Module Def', 'Schools') and not dataent.db.exists('Module Def', 'Education'):
		dataent.rename_doc("Module Def", "Schools", "Education")

	# delete the school module
	if dataent.db.exists('Module Def', 'Schools') and dataent.db.exists('Module Def', 'Education'):
		dataent.db.sql("""delete from `tabModule Def` where module_name = 'Schools'""")


	# rename "School Settings" to the "Education Settings
	if dataent.db.exists('DocType', 'School Settings'):
		dataent.rename_doc("DocType", "School Settings", "Education Settings", force=True)
		dataent.reload_doc("education", "doctype", "education_settings")

	# delete the discussion web form if exists
	if dataent.db.exists('Web Form', 'Discussion'):
		dataent.db.sql("""delete from `tabWeb Form` where name = 'discussion'""")

	# rename the select option field from "School Bus" to "Institute's Bus"
	dataent.reload_doc("education", "doctype", "Program Enrollment")
	if "mode_of_transportation" in dataent.db.get_table_columns("Program Enrollment"):
		dataent.db.sql("""update `tabProgram Enrollment` set mode_of_transportation = "Institute's Bus"
			where mode_of_transportation = "School Bus" """)
