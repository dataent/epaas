# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

from dataent.model.document import Document
from dataent.model.naming import set_name_by_naming_series

class Campaign(Document):
	def autoname(self):
		if dataent.defaults.get_global_default('campaign_naming_by') != 'Naming Series':
			self.name = self.campaign_name
		else:
			set_name_by_naming_series(self)
