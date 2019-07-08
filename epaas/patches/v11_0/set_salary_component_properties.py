from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doc('hr', 'doctype', 'salary_detail')
	dataent.reload_doc('hr', 'doctype', 'salary_component')

	dataent.db.sql("update `tabSalary Component` set is_payable=1, is_tax_applicable=1 where type='Earning'")
	dataent.db.sql("update `tabSalary Component` set is_payable=0 where type='Deduction'")

	dataent.db.sql("""update `tabSalary Component` set variable_based_on_taxable_salary=1
	    where type='Deduction' and name in ('TDS', 'Tax Deducted at Source')""")

	dataent.db.sql("""update `tabSalary Detail` set is_tax_applicable=1
	    where parentfield='earnings' and statistical_component=0""")
	dataent.db.sql("""update `tabSalary Detail` set variable_based_on_taxable_salary=1
	    where parentfield='deductions' and salary_component in ('TDS', 'Tax Deducted at Source')""")