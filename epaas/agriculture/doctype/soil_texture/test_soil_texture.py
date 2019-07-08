# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import dataent
import unittest

class TestSoilTexture(unittest.TestCase):
	def test_texture_selection(self):
		soil_tex = dataent.get_all('Soil Texture', fields=['name'], filters={'collection_datetime': '2017-11-08'})
		doc = dataent.get_doc('Soil Texture', soil_tex[0].name)
		self.assertEqual(doc.silt_composition, 50)
		self.assertEqual(doc.soil_type, 'Silt Loam')