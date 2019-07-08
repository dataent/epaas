# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
from dataent.utils import cint
from dateutil.relativedelta import relativedelta

class ManufacturingSettings(Document):
	pass

def get_mins_between_operations():
	return relativedelta(minutes=cint(dataent.db.get_single_value("Manufacturing Settings",
		"mins_between_operations")) or 10)

@dataent.whitelist()
def is_material_consumption_enabled():
	if not hasattr(dataent.local, 'material_consumption'):
		dataent.local.material_consumption = cint(dataent.db.get_single_value('Manufacturing Settings',
			'material_consumption'))

	return dataent.local.material_consumption