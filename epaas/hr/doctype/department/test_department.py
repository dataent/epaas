# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
from __future__ import unicode_literals
import dataent
import unittest

test_ignore = ["Leave Block List"]
class TestDepartment(unittest.TestCase):
    def test_remove_department_data(self):
        doc = create_department("Test Department")
        dataent.delete_doc('Department', doc.name)

def create_department(department_name, parent_department=None):
    doc = dataent.get_doc({
        'doctype': 'Department',
        'is_group': 0,
        'parent_department': parent_department,
        'department_name': department_name,
        'company': dataent.defaults.get_defaults().company
    }).insert()

    return doc

test_records = dataent.get_test_records('Department')