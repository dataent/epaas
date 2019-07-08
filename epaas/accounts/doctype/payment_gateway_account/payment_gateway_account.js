cur_frm.cscript.refresh = function(doc, dt, dn){
	if(!doc.__islocal){
		var df = dataent.meta.get_docfield(doc.doctype, "payment_gateway", doc.name);
		df.read_only = 1;
	}
}