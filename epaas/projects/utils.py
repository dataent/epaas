# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import dataent

@dataent.whitelist()
def query_task(doctype, txt, searchfield, start, page_len, filters):
	from dataent.desk.reportview import build_match_conditions

	search_string = "%%%s%%" % txt
	order_by_string = "%s%%" % txt
	match_conditions = build_match_conditions("Task")
	match_conditions = ("and" + match_conditions) if match_conditions else ""

	return dataent.db.sql("""select name, subject from `tabTask`
		where (`%s` like %s or `subject` like %s) %s
		order by
			case when `subject` like %s then 0 else 1 end,
			case when `%s` like %s then 0 else 1 end,
			`%s`,
			subject
		limit %s, %s""" %
		(dataent.db.escape(searchfield), "%s", "%s", match_conditions, "%s",
			dataent.db.escape(searchfield), "%s", dataent.db.escape(searchfield), "%s", "%s"),
		(search_string, search_string, order_by_string, order_by_string, start, page_len))
