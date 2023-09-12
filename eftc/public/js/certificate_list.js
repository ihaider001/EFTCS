frappe.listview_settings['Certificate'] = {
    onload: function(listview) {
            // Changing the name of Id from listview
            $(".level-item:contains('ID')").text("Certificate Id");
            
    }
}; 