// Copyright (c) 2022, shridhar.p@zerodha..com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Conference', {
	refresh: function(frm) {
		frm.dashboard.add_comment("Upload all inages as public, as private files fails to load on website", "red", true)
	}
});
