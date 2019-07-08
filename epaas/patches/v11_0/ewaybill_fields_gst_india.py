from __future__ import unicode_literals
import dataent
from epaas.regional.india.setup import make_custom_fields

def execute():
    company = dataent.get_all('Company', filters = {'country': 'India'})
    if not company:
        return

    make_custom_fields()