from __future__ import unicode_literals
import dataent
from epaas.regional.india.setup import setup

def execute():
	company = dataent.get_all('Company', filters = {'country': 'India'})
	if not company:
		return

	# call setup for india
	setup(patch=True)