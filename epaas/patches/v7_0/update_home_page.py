from __future__ import unicode_literals
import dataent
import epaas

def execute():
	dataent.reload_doc('portal', 'doctype', 'homepage_featured_product')
	dataent.reload_doc('portal', 'doctype', 'homepage')
	dataent.reload_doc('portal', 'doctype', 'products_settings')
	dataent.reload_doctype('Item')
	dataent.reload_doctype('Item Group')

	website_settings = dataent.get_doc('Website Settings', 'Website Settings')
	if dataent.db.exists('Web Page', website_settings.home_page):
		header = dataent.db.get_value('Web Page', website_settings.home_page, 'header')
		if header and header.startswith("<div class='hero text-center'>"):
			homepage = dataent.get_doc('Homepage', 'Homepage')
			homepage.company = epaas.get_default_company() or dataent.get_all("Company")[0].name
			if '<h1>' in header:
				homepage.tag_line = header.split('<h1>')[1].split('</h1>')[0] or 'Default Website'
			else:
				homepage.tag_line = 'Default Website'
			homepage.setup_items()
			homepage.save()

			website_settings.home_page = 'home'
			website_settings.save()

