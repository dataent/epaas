# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	for doctype in ("Material Request", "Purchase Order"):
		dataent.reload_doctype(doctype)
		dataent.reload_doctype(doctype + " Item")

		if not dataent.db.has_column(doctype, "schedule_date"):
			continue

		#Update only submitted MR
		for record in dataent.get_all(doctype, filters= [["docstatus", "=", 1]], fields=["name"]):
			doc = dataent.get_doc(doctype, record)
			if doc.items:
				if not doc.schedule_date:
					schedule_dates = [d.schedule_date for d in doc.items if d.schedule_date]
					if len(schedule_dates) > 0:
						min_schedule_date = min(schedule_dates)
						dataent.db.set_value(doctype, record,
							"schedule_date", min_schedule_date, update_modified=False)