# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent

@dataent.whitelist()
def enable_hub():
	hub_settings = dataent.get_doc('Marketplace Settings')
	hub_settings.register()
	dataent.db.commit()
	return hub_settings

@dataent.whitelist()
def sync():
	hub_settings = dataent.get_doc('Marketplace Settings')
	hub_settings.sync()
