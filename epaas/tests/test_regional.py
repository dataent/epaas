from __future__ import unicode_literals
import unittest, dataent, epaas

@epaas.allow_regional
def test_method():
	return 'original'

class TestInit(unittest.TestCase):
	def test_regional_overrides(self):
		dataent.flags.country = 'India'
		self.assertEqual(test_method(), 'overridden')

		dataent.flags.country = 'Maldives'
		self.assertEqual(test_method(), 'original')

		dataent.flags.country = 'France'
		self.assertEqual(test_method(), 'overridden')