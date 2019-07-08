# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest

test_dependencies = ["Fertilizer"]

class TestCrop(unittest.TestCase):
	def test_crop_period(self):
		basil = dataent.get_doc('Crop', 'Basil from seed')
		self.assertEqual(basil.period, 15)