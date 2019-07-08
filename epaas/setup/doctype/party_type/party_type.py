# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document

class PartyType(Document):
	pass

@dataent.whitelist()
def get_party_type(doctype, txt, searchfield, start, page_len, filters):
	cond = ''
	if filters and filters.get('account'):
		account_type = dataent.db.get_value('Account', filters.get('account'), 'account_type')
		cond = "and account_type = '%s'" % account_type

	return dataent.db.sql("""select name from `tabParty Type`
			where `{key}` LIKE %(txt)s {cond}
			order by name limit %(start)s, %(page_len)s"""
			.format(key=searchfield, cond=cond), {
				'txt': "%%%s%%" % dataent.db.escape(txt),
				'start': start, 'page_len': page_len
			})
