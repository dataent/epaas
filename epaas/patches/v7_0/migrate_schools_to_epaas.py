from __future__ import unicode_literals
import dataent, os
from dataent.installer import remove_from_installed_apps

def execute():
	reload_doctypes_for_schools_icons()

	dataent.reload_doc('website', 'doctype', 'portal_settings')
	dataent.reload_doc('website', 'doctype', 'portal_menu_item')
	dataent.reload_doc('buying', 'doctype', 'request_for_quotation')

	if 'schools' in dataent.get_installed_apps():
		dataent.db.sql("""delete from `tabDesktop Icon`""")
		
		if not dataent.db.exists('Module Def', 'Schools') and dataent.db.exists('Module Def', 'Academics'):
			
			# 'Schools' module changed to the 'Education'
			# dataent.rename_doc("Module Def", "Academics", "Schools")
			
			dataent.rename_doc("Module Def", "Academics", "Education")
			
		remove_from_installed_apps("schools")

def reload_doctypes_for_schools_icons():
	# 'Schools' module changed to the 'Education'
	# base_path = dataent.get_app_path('epaas', 'schools', 'doctype')
	
	base_path = dataent.get_app_path('epaas', 'education', 'doctype')
	for doctype in os.listdir(base_path):
		if os.path.exists(os.path.join(base_path, doctype, doctype + '.json')) \
			and doctype not in ("fee_component", "assessment", "assessment_result"):
			dataent.reload_doc('education', 'doctype', doctype)