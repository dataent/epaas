from __future__ import unicode_literals
import unittest

import dataent


class TestAccountsSettings(unittest.TestCase):
	def tearDown(self):
		# Just in case `save` method succeeds, we need to take things back to default so that other tests
		# don't break
		cur_settings = dataent.get_doc('Accounts Settings', 'Accounts Settings')
		cur_settings.allow_stale = 1
		cur_settings.save()

	def test_stale_days(self):
		cur_settings = dataent.get_doc('Accounts Settings', 'Accounts Settings')
		cur_settings.allow_stale = 0
		cur_settings.stale_days = 0

		self.assertRaises(dataent.ValidationError, cur_settings.save)

		cur_settings.stale_days = -1
		self.assertRaises(dataent.ValidationError, cur_settings.save)
