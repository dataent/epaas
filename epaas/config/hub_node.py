from __future__ import unicode_literals
from dataent import _

def get_data():
	return [
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Marketplace Settings"
				},
			]
		},
		{
			"label": _("Marketplace"),
			"items": [
				{
					"type": "page",
					"name": "marketplace/home"
				},
			]
		},
	]