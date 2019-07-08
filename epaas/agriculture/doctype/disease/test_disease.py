# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest

class TestDisease(unittest.TestCase):
	def test_treatment_period(self):
		disease = dataent.get_doc('Disease', 'Aphids')
		self.assertEqual(disease.treatment_period, 3)