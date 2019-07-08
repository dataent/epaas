# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from __future__ import unicode_literals
import unittest
import dataent

test_records = dataent.get_test_records('BOM')

class TestBOMUpdateTool(unittest.TestCase):
	def test_replace_bom(self):
		current_bom = "BOM-_Test Item Home Desktop Manufactured-001"

		bom_doc = dataent.copy_doc(test_records[0])
		bom_doc.items[1].item_code = "_Test Item"
		bom_doc.insert()

		update_tool = dataent.get_doc("BOM Update Tool")
		update_tool.current_bom = current_bom
		update_tool.new_bom = bom_doc.name
		update_tool.replace_bom()

		self.assertFalse(dataent.db.sql("select name from `tabBOM Item` where bom_no=%s", current_bom))
		self.assertTrue(dataent.db.sql("select name from `tabBOM Item` where bom_no=%s", bom_doc.name))

		# reverse, as it affects other testcases
		update_tool.current_bom = bom_doc.name
		update_tool.new_bom = current_bom
		update_tool.replace_bom()