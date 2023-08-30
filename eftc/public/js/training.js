
frappe.ui.form.on("Training Schedule", {
    refresh: function(frm) {
        frm.fields_dict['attendees'].grid.get_field('validity').get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['value', 'in', ['1', '2']]
                ]
            };
        };
    }
});

frappe.ui.form.on("Attendees Table", {
    issue_date: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        var issue_date = child.issue_date;
        var validity = child.validity;

        if (issue_date && validity === '1') {
            var expiry_date = new Date(issue_date);
            expiry_date.setFullYear(expiry_date.getFullYear() + 1);
            frappe.model.set_value(child.doctype, child.name, 'expiry_date', expiry_date);
        }
    },
    validity: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        var issue_date = child.issue_date;
        var validity = child.validity;

        if (issue_date) {
            var expiry_date = new Date(issue_date);
            
            if (validity === '1') {
                expiry_date.setFullYear(expiry_date.getFullYear() + 1);
            } else if (validity === '2') {
                expiry_date.setFullYear(expiry_date.getFullYear() + 2);
            }
            frappe.model.set_value(child.doctype, child.name, 'expiry_date', expiry_date);
        }
    }
});
