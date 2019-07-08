from __future__ import unicode_literals

import dataent, sys
import epaas
import dataent.utils
from epaas.demo.user import hr, sales, purchase, manufacturing, stock, accounts, projects, fixed_asset
from epaas.demo.user import education as edu
from epaas.demo.setup import education, manufacture, setup_data, healthcare, retail
"""
Make a demo

1. Start with a fresh account

bench --site demo.epaas.dev reinstall

2. Install Demo

bench --site demo.epaas.dev execute epaas.demo.demo.make

3. If Demo breaks, to continue

bench --site demo.epaas.dev execute epaas.demo.demo.simulate

"""

def make(domain='Manufacturing', days=100):
	dataent.flags.domain = domain
	dataent.flags.mute_emails = True
	setup_data.setup(domain)
	if domain== 'Manufacturing':
		manufacture.setup_data()
	elif domain == "Retail":
		retail.setup_data()
	elif domain== 'Education':
		education.setup_data()
	elif domain== 'Healthcare':
		healthcare.setup_data()

	site = dataent.local.site
	dataent.destroy()
	dataent.init(site)
	dataent.connect()

	simulate(domain, days)

def simulate(domain='Manufacturing', days=100):
	runs_for = dataent.flags.runs_for or days
	dataent.flags.company = epaas.get_default_company()
	dataent.flags.mute_emails = True

	if not dataent.flags.start_date:
		# start date = 100 days back
		dataent.flags.start_date = dataent.utils.add_days(dataent.utils.nowdate(),
			-1 * runs_for)

	current_date = dataent.utils.getdate(dataent.flags.start_date)

	# continue?
	demo_last_date = dataent.db.get_global('demo_last_date')
	if demo_last_date:
		current_date = dataent.utils.add_days(dataent.utils.getdate(demo_last_date), 1)

	# run till today
	if not runs_for:
		runs_for = dataent.utils.date_diff(dataent.utils.nowdate(), current_date)
		# runs_for = 100

	fixed_asset.work()
	for i in range(runs_for):
		sys.stdout.write("\rSimulating {0}: Day {1}".format(
			current_date.strftime("%Y-%m-%d"), i))
		sys.stdout.flush()
		dataent.flags.current_date = current_date
		if current_date.weekday() in (5, 6):
			current_date = dataent.utils.add_days(current_date, 1)
			continue
		try:
			hr.work()
			purchase.work()
			stock.work()
			accounts.work()
			projects.run_projects(current_date)
			sales.work(domain)
			# run_messages()

			if domain=='Manufacturing':
				manufacturing.work()
			elif domain=='Education':
				edu.work()

		except:
			dataent.db.set_global('demo_last_date', current_date)
			raise
		finally:
			current_date = dataent.utils.add_days(current_date, 1)
			dataent.db.commit()
