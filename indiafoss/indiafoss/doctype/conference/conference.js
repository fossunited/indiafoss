// Copyright (c) 2022, shridhar.p@zerodha..com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Conference', {
	refresh: function(frm) {
		frm.dashboard.add_comment("Upload all images as public, as private files fails to load on website", "red", true)
	        frm.sidebar.add_user_action("See on Website", function(){
	        }).attr("href", "/" + frm.doc.city + '/' + frm.doc.year).attr("target", "_blank")
	},
	end_date: function(frm){
		if(frm.doc.end_date && frm.doc.start_date > frm.doc.end_date){
			frm.set_value('end_date', '')
			frappe.throw('End Date should be greater then start date')
		}
	},

	start_date: function(frm){
		if(frm.doc.start_date && frm.doc.start_date > frm.doc.end_date){
			frm.set_value('start_date', '')
			frappe.throw('Start Date should be less then end date')
		}
	},

	start_time: function(frm){
		if(frm.doc.start_time && frm.doc.start_time > frm.doc.end_time){
			frm.set_value('start_time', '')
			frm.refresh_field('start_time');

			frappe.throw('Start Time should be less then end time')
		}
	},

	end_time: function(frm){
		if(frm.doc.end_time && frm.doc.end_time < frm.doc.start_time){
			frm.set_value('end_time', '')
			frm.refresh_field('end_time');

			frappe.throw('End Time should be greater then start time')
		}
	}
});
