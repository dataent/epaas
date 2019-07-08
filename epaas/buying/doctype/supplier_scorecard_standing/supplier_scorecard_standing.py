# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document

class SupplierScorecardStanding(Document):
	pass


@dataent.whitelist()
def get_scoring_standing(standing_name):
	standing = dataent.get_doc("Supplier Scorecard Standing", standing_name)

	return standing


@dataent.whitelist()
def get_standings_list():
	standings = dataent.db.sql("""
		SELECT
			scs.name
		FROM
			`tabSupplier Scorecard Standing` scs""",
			{}, as_dict=1)

	return standings