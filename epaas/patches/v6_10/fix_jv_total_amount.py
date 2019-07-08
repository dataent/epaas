from __future__ import unicode_literals
import dataent

# patch all for-print field (total amount) in Journal Entry in 2015
def execute():
	for je in dataent.get_all("Journal Entry", filters={"creation": (">", "2015-01-01")}):
		je = dataent.get_doc("Journal Entry", je.name)
		original = je.total_amount

		je.set_print_format_fields()

		if je.total_amount != original:
			je.db_set("total_amount", je.total_amount, update_modified=False)
			je.db_set("total_amount_in_words", je.total_amount_in_words, update_modified=False)