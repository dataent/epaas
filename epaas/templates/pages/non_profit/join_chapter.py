from __future__ import unicode_literals
import dataent

def get_context(context):
	context.no_cache = True
	chapter = dataent.get_doc('Chapter', dataent.form_dict.name)
	if dataent.session.user!='Guest':
		if dataent.session.user in [d.user for d in chapter.members if d.enabled == 1]:
			context.already_member = True
		else:
			if dataent.request.method=='GET':
				pass
			elif dataent.request.method=='POST':
				chapter.append('members', dict(
					user=dataent.session.user,
					introduction=dataent.form_dict.introduction,
					website_url=dataent.form_dict.website_url,
					enabled=1
				))
				chapter.save(ignore_permissions=1)
				dataent.db.commit()

	context.chapter = chapter
