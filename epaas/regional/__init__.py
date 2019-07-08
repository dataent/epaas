# Copyright (c) 2018, Dataent Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from epaas import get_region

def check_deletion_permission(doc, method):
	region = get_region()
	if region in ["Nepal", "France"] and doc.docstatus != 0:
		dataent.throw(_("Deletion is not permitted for country {0}".format(region)))
