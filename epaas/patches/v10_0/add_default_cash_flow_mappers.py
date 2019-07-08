# Copyright (c) 2017, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import dataent
from epaas.setup.install import create_default_cash_flow_mapper_templates


def execute():
    dataent.reload_doc('accounts', 'doctype', dataent.scrub('Cash Flow Mapping'))
    dataent.reload_doc('accounts', 'doctype', dataent.scrub('Cash Flow Mapper'))
    dataent.reload_doc('accounts', 'doctype', dataent.scrub('Cash Flow Mapping Template Details'))

    create_default_cash_flow_mapper_templates()
