frappe.ui.form.on("Sales Invoice", {
  refresh:function(frm) {
        frm.fields_dict['rounding_adjustment'].df.hidden = 1; 
        frm.fields_dict['rounded_total'].df.hidden = 1;
        frm.refresh_field("rounding_adjustment"); 
        frm.refresh_field("rounded_total");
        frm.page.add_inner_button(__("Training Schedue"), function() {
          frappe.db.get_value("Sales Order",frm.doc.items[0].sales_order, "custom_vat_number").then(r=> {
          frm.set_value("custom_vat_number_",r.message.custom_vat_number)
          frm.refresh_field("custom_vat_number_")
        });
          frappe.call({
            method: "eftc.eftc_app.doctype.training_schedule.training_schedule.get_training_schedule",
            args: {
              sales_order: frm.doc.items[0]["sales_order"],
                // Add any additional arguments as needed
            },
            callback: function(response) {
                // Handle the response here
                if (response.message) {
                  let dialog = new frappe.ui.Dialog({
                    title: 'Training Schedule',
                    size: "large",
                    fields: [
                      {
                          fieldtype: 'Table',
                          cannot_add_rows: true,
                           in_place_edit: true,
                          data:response.message,
                          fields: [
                              { fieldname: 'name', fieldtype: 'Data', in_list_view: 1, label: 'Name',width:2 },
                              { fieldname: 'customer', fieldtype: 'Data', in_list_view: 1, label: 'Customer',width:2 }
                              
                          ],
                          

                      },
                      
                  ],
                  primary_action_label: __('Get Training Schedule'),
                          primary_action: (values) => {
                            frappe.call({
                                            method: "eftc.eftc_app.doctype.training_schedule.training_schedule.get_attendee",
                                            args:{
                                              'values':values["undefined"],
                                              "sales_invoice":cur_frm.doc.items
                                            },
                                            callback:function(response){
                                              for ( var attendee in response.message[0]){ 
                                              var child_table = cur_frm.add_child('attendee', {
                                                iqamaid_no: response.message[0][attendee]["iqamaid_no"],
                                                attendee_name: response.message[0][attendee]["attendee_name"]
                                            //     // Add more fields as needed
                                            });
                                              }
                                              cur_frm.doc.items.forEach(function(item) {
                                                // Assuming `item_code` is the property you want to match with your data
                                                var matchingData = response.message[1].find(function(data) {
                                                    return data.item_code === item.item_code;
                                                });
                                            
                                                if (matchingData) {
                                                    // Update the custom_training_schedule field
                                                    frappe.model.set_value(item.doctype, item.name, 'custom_training_schedule', matchingData.custom_training_schedule);
                                                }
                                            });
                                            
                                              frm.refresh_field("attendee");
                                              frm.refresh_field("items")
                                            }
                                        })
                            dialog.hide();
                            }
                  
                  });dialog.show();
                  dialog.$wrapper.find('.modal-dialog').css("max-width", "1000px");
                } else {
                    console.error("Error:", response.exc);
                }
            }
        });

      }, __("Get Items From"));
    },
    customer_address : function (frm) {
      if (cur_frm.doc.customer_address){
       frappe.db.get_doc("Address",cur_frm.doc.customer_address).then(r=>{
        cur_frm.set_value("custom_cr_number",r.cr_no)
        cur_frm.set_value("custom_vat_number_",r.vat_number_)
       })
        }
   },
})