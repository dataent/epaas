# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent, unittest

from epaas.accounts.doctype.fiscal_year.fiscal_year import FiscalYearIncorrectDate

test_records = dataent.get_test_records('Fiscal Year')
test_ignore = ["Company"]

class TestFiscalYear(unittest.TestCase):
	def test_extra_year(self):
		if dataent.db.exists("Fiscal Year", "_Test Fiscal Year 2000"):
			dataent.delete_doc("Fiscal Year", "_Test Fiscal Year 2000")

		fy = dataent.get_doc({
			"doctype": "Fiscal Year",
			"year": "_Test Fiscal Year 2000",
			"year_end_date": "2002-12-31",
			"year_start_date": "2000-04-01"
		})

		self.assertRaises(FiscalYearIncorrectDate, fy.insert)
