# # -*- coding: utf-8 -*-
# # Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# # For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.document import Document
import dataent.utils
from dataent import _
from epaas.hr.doctype.daily_work_summary.daily_work_summary import get_user_emails_from_group

class DailyWorkSummaryGroup(Document):
	def validate(self):
		if self.users:
			if not dataent.flags.in_test and not is_incoming_account_enabled():
				dataent.throw(_('Please enable default incoming account before creating Daily Work Summary Group'))


def trigger_emails():
	'''Send emails to Employees at the given hour asking
			them what did they work on today'''
	groups = dataent.get_all("Daily Work Summary Group")
	for d in groups:
		group_doc = dataent.get_doc("Daily Work Summary Group", d)
		if (is_current_hour(group_doc.send_emails_at)
			and not is_holiday_today(group_doc.holiday_list)
			and group_doc.enabled):
			emails = get_user_emails_from_group(group_doc)
			# find emails relating to a company
			if emails:
				daily_work_summary = dataent.get_doc(
					dict(doctype='Daily Work Summary', daily_work_summary_group=group_doc.name)
				).insert()
				daily_work_summary.send_mails(group_doc, emails)


def is_current_hour(hour):
	return dataent.utils.nowtime().split(':')[0] == hour.split(':')[0]


def is_holiday_today(holiday_list):
	date = dataent.utils.today()
	if holiday_list:
		return dataent.get_all('Holiday List',
			dict(name=holiday_list, holiday_date=date)) and True or False
	else:
		return False


def send_summary():
	'''Send summary to everyone'''
	for d in dataent.get_all('Daily Work Summary', dict(status='Open')):
		daily_work_summary = dataent.get_doc('Daily Work Summary', d.name)
		daily_work_summary.send_summary()


def is_incoming_account_enabled():
	return dataent.db.get_value('Email Account', dict(enable_incoming=1, default_incoming=1))
