# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals
import unittest

import dataent


class TestPaymentTermsTemplate(unittest.TestCase):
	def tearDown(self):
		dataent.delete_doc('Payment Terms Template', '_Test Payment Terms Template For Test', force=1)

	def test_create_template(self):
		template = dataent.get_doc({
			'doctype': 'Payment Terms Template',
			'template_name': '_Test Payment Terms Template For Test',
			'terms': [{
				'doctype': 'Payment Terms Template Detail',
				'invoice_portion': 50.00,
				'credit_days_based_on': 'Day(s) after invoice date',
				'credit_days': 30
			}]
		})

		self.assertRaises(dataent.ValidationError, template.insert)

		template.append('terms', {
			'doctype': 'Payment Terms Template Detail',
			'invoice_portion': 50.00,
			'credit_days_based_on': 'Day(s) after invoice date',
			'credit_days': 0
		})

		template.insert()

	def test_credit_days(self):
		template = dataent.get_doc({
			'doctype': 'Payment Terms Template',
			'template_name': '_Test Payment Terms Template For Test',
			'terms': [{
				'doctype': 'Payment Terms Template Detail',
				'invoice_portion': 100.00,
				'credit_days_based_on': 'Day(s) after invoice date',
				'credit_days': -30
			}]
		})

		self.assertRaises(dataent.ValidationError, template.insert)

	def test_duplicate_terms(self):
		template = dataent.get_doc({
			'doctype': 'Payment Terms Template',
			'template_name': '_Test Payment Terms Template For Test',
			'terms': [
				{
					'doctype': 'Payment Terms Template Detail',
					'invoice_portion': 50.00,
					'credit_days_based_on': 'Day(s) after invoice date',
					'credit_days': 30
				},
				{
					'doctype': 'Payment Terms Template Detail',
					'invoice_portion': 50.00,
					'credit_days_based_on': 'Day(s) after invoice date',
					'credit_days': 30
				}

			]
		})

		self.assertRaises(dataent.ValidationError, template.insert)
