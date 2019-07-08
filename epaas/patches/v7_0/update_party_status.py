from __future__ import unicode_literals
import dataent

def execute():
	return
	# for party_type in ('Customer', 'Supplier'):
	# 	dataent.reload_doctype(party_type)
	#
	# 	# set all as default status
	# 	dataent.db.sql('update `tab{0}` set status=%s'.format(party_type), default_status[party_type])
	#
	# 	for doctype in status_depends_on[party_type]:
	# 		filters = get_filters_for(doctype)
	# 		parties = dataent.get_all(doctype, fields="{0} as party".format(party_type.lower()),
	# 			filters=filters, limit_page_length=1)
	#
	# 		parties = filter(None, [p.party for p in parties])
	#
	# 		if parties:
	# 			dataent.db.sql('update `tab{0}` set status="Open" where name in ({1})'.format(party_type,
	# 				', '.join(len(parties) * ['%s'])), parties)