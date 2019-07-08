# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
import re

def execute():
	for name, html in dataent.db.sql("""select name, html from `tabPrint Format`
		where standard = 'No' and html like '%%purchase\\_tax\\_details%%'"""):
			html = re.sub(r"\bpurchase_tax_details\b", "taxes", html)
			dataent.db.set_value("Print Format", name, "html", html)
