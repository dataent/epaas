# Copyright (c) 2016, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt

from __future__ import unicode_literals

from dataent.utils.bot import BotParser

import dataent
from dataent import _

class FindItemBot(BotParser):
	def get_reply(self):
		if self.startswith('where is', 'find item', 'locate'):
			if not dataent.has_permission('Warehouse'):
				raise dataent.PermissionError

			item = '%{0}%'.format(self.strip_words(self.query, 'where is', 'find item', 'locate'))
			items = dataent.db.sql('''select name from `tabItem` where item_code like %(txt)s
				or item_name like %(txt)s or description like %(txt)s''', dict(txt=item))

			if items:
				out = []
				warehouses = dataent.get_all("Warehouse")
				for item in items:
					found = False
					for warehouse in warehouses:
						qty = dataent.db.get_value("Bin", {'item_code': item[0], 'warehouse': warehouse.name}, 'actual_qty')
						if qty:
							out.append(_('{0} units of [{1}](#Form/Item/{1}) found in [{2}](#Form/Warehouse/{2})').format(qty,
								item[0], warehouse.name))
							found = True

					if not found:
						out.append(_('[{0}](#Form/Item/{0}) is out of stock').format(item[0]))

				return "\n\n".join(out)

			else:
				return _("Did not find any item called {0}".format(item))