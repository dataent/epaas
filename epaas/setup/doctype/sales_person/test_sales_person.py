# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals

test_dependencies = ["Employee"]

import dataent
test_records = dataent.get_test_records('Sales Person')

test_ignore = ["Item Group"]
