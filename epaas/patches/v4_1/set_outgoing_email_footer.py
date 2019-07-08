# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from epaas.setup.install import default_mail_footer

def execute():
	return
	mail_footer = dataent.db.get_default('mail_footer') or ''
	mail_footer += default_mail_footer
	dataent.db.set_value("Outgoing Email Settings", "Outgoing Email Settings", "footer", mail_footer)
