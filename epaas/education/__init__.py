from __future__ import unicode_literals
import dataent
from dataent import _

class StudentNotInGroupError(dataent.ValidationError): pass

def validate_student_belongs_to_group(student, student_group):
	groups = dataent.db.get_all('Student Group Student', ['parent'], dict(student = student, active=1))
	if not student_group in [d.parent for d in groups]:
		dataent.throw(_('Student {0} does not belong to group {1}').format(dataent.bold(student), dataent.bold(student_group)),
			StudentNotInGroupError)
