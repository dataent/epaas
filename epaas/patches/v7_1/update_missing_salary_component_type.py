from __future__ import unicode_literals

import dataent
from dataent.utils import cstr

'''
Some components do not have type set, try and guess whether they turn up in
earnings or deductions in existing salary slips
'''

def execute():
	dataent.reload_doc("accounts", "doctype", "salary_component_account")
	dataent.reload_doc("hr", "doctype", "salary_component")
	dataent.reload_doc("hr", "doctype", "taxable_salary_slab")
	
	for s in dataent.db.sql('''select name, type, salary_component_abbr from `tabSalary Component` 
			where ifnull(type, "")="" or ifnull(salary_component_abbr, "") = ""''', as_dict=1):
			
		component = dataent.get_doc('Salary Component', s.name)

		# guess
		if not s.type:
			guess = dataent.db.sql('''select
				parentfield from `tabSalary Detail`
				where salary_component=%s limit 1''', s.name)

			if guess:
				component.type = 'Earning' if guess[0][0]=='earnings' else 'Deduction'

			else:
				component.type = 'Deduction'
				
		if not s.salary_component_abbr:
			abbr = ''.join([c[0] for c in component.salary_component.split()]).upper()
			
			abbr_count = dataent.db.sql("""
				select 
					count(name) 
				from 
					`tabSalary Component` 
				where 
					salary_component_abbr = %s or salary_component_abbr like %s
				""", (abbr, abbr + "-%%"))
				
			if abbr_count and abbr_count[0][0] > 0:
				abbr = abbr + "-" + cstr(abbr_count[0][0])
				
			component.salary_component_abbr = abbr
			
		component.save()