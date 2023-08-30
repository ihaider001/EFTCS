
frappe.listview_settings['Training Schedule'] = {
    onload: function(listview) {
            listview.page.add_inner_button('Show Calender', function() {
            frappe.set_route("/app/training-schedule/view/calendar/Training%20Schedule%20List")
            }).addClass("btn-warning").css({'color':'blue','font-weight': 'bold','background':'white'});
    }
}; 
