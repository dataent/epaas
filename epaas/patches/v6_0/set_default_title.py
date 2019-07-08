from __future__ import unicode_literals
import dataent

def execute():
	dataent.reload_doctype("Quotation")
	dataent.db.sql("""update tabQuotation set title = customer_name""")

	dataent.reload_doctype("Sales Order")
	dataent.db.sql("""update `tabSales Order` set title = customer_name""")

	dataent.reload_doctype("Delivery Note")
	dataent.db.sql("""update `tabDelivery Note` set title = customer_name""")

	dataent.reload_doctype("Material Request")
	dataent.db.sql("""update `tabMaterial Request` set title = material_request_type""")

	dataent.reload_doctype("Supplier Quotation")
	dataent.db.sql("""update `tabSupplier Quotation` set title = supplier_name""")

	dataent.reload_doctype("Purchase Order")
	dataent.db.sql("""update `tabPurchase Order` set title = supplier_name""")

	dataent.reload_doctype("Purchase Receipt")
	dataent.db.sql("""update `tabPurchase Receipt` set title = supplier_name""")

	dataent.reload_doctype("Purchase Invoice")
	dataent.db.sql("""update `tabPurchase Invoice` set title = supplier_name""")

	dataent.reload_doctype("Stock Entry")
	dataent.db.sql("""update `tabStock Entry` set title = purpose""")

	dataent.reload_doctype("Sales Invoice")
	dataent.db.sql("""update `tabSales Invoice` set title = customer_name""")

	dataent.reload_doctype("Expense Claim")
	dataent.db.sql("""update `tabExpense Claim` set title = employee_name""")
