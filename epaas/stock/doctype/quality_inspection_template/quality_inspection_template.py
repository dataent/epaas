# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document

class QualityInspectionTemplate(Document):
	pass

def get_template_details(template):
	if not template: return []

	return dataent.get_all('Item Quality Inspection Parameter', fields=["specification", "value"],
		filters={'parenttype': 'Quality Inspection Template', 'parent': template}, order_by="idx")