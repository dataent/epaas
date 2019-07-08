from __future__ import unicode_literals
import dataent
from dataent.utils import flt

def execute():
	dataent.reload_doc('hr', 'doctype', 'salary_component')
	sal_components = dataent.db.sql("""
		select DISTINCT salary_component, parentfield from `tabSalary Detail`""", as_dict=True)

	if sal_components:
		for sal_component in sal_components:
			if sal_component.parentfield == "earnings":
				dataent.db.sql("""update `tabSalary Component` set type='Earning' where salary_component=%(sal_comp)s""",{"sal_comp": sal_component.salary_component})
			else:
				dataent.db.sql("""update `tabSalary Component` set type='Deduction' where salary_component=%(sal_comp)s""",{"sal_comp": sal_component.salary_component})