from __future__ import print_function, unicode_literals
import dataent

def execute():
	dataent.reload_doctype("File")
	dataent.reload_doctype("Item")
	for item in dataent.get_all("Item", fields=("name", "website_image", "thumbnail")):
		if item.website_image and not item.thumbnail:
			item_doc = dataent.get_doc("Item", item.name)
			try:
				item_doc.make_thumbnail()
				if item_doc.thumbnail:
					item_doc.db_set("thumbnail", item_doc.thumbnail, update_modified=False)
			except Exception:
				print("Unable to make thumbnail for {0}".format(item.website_image.encode("utf-8")))
