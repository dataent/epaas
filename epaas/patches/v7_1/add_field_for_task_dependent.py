from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype('Task')
	for t in dataent.get_all('Task', fields=['name']):
		task = dataent.get_doc('Task', t.name)
		task.update_depends_on()
		if task.depends_on_tasks:
			task.db_set('depends_on_tasks', task.depends_on_tasks, update_modified=False)
