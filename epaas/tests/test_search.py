from __future__ import unicode_literals
import unittest
import dataent
from dataent.contacts.address_and_contact import filter_dynamic_link_doctypes

class TestSearch(unittest.TestCase):
	#Search for the word "clie", part of the word "client" (customer) in french.
	def test_contact_search_in_foreign_language(self):
		dataent.local.lang = 'fr'
		output = filter_dynamic_link_doctypes("DocType", "clie", "name", 0, 20, {'fieldtype': 'HTML', 'fieldname': 'contact_html'})

		result = [['found' for x in y if x=="Customer"] for y in output]
		self.assertTrue(['found'] in result)

	def tearDown(self):
		dataent.local.lang = 'en'