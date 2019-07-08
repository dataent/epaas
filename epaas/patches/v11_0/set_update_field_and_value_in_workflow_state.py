from __future__ import unicode_literals
import dataent
from dataent.model.workflow import get_workflow_name

def execute():
	for doctype in ['Expense Claim', 'Leave Application']:

		active_workflow = get_workflow_name(doctype)
		if not active_workflow: continue

		workflow_states = dataent.get_all('Workflow Document State',
			filters=[['parent', '=', active_workflow]],
			fields=['*'])

		for state in workflow_states:
			if state.update_field: continue
			status_field = 'approval_status' if doctype=="Expense Claim" else 'status'
			dataent.set_value('Workflow Document State', state.name, 'update_field', status_field)
			dataent.set_value('Workflow Document State', state.name, 'update_value', state.state)
