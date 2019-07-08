# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.utils import cint
from epaas.stock.stock_balance import repost

def execute():
	if cint(dataent.db.get_value("Stock Settings", None, "allow_negative_stock")):
		repost(only_actual=True)