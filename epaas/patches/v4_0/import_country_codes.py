# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.geo.country_info import get_all
from dataent.utils.install import import_country_and_currency

from six import iteritems

def execute():
	dataent.reload_doc("setup", "doctype", "country")
	import_country_and_currency()
	for name, country in iteritems(get_all()):
		dataent.set_value("Country", name, "code", country.get("code"))