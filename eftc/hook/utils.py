import  frappe


def permission_query_for_training_schedule(user):
    if not user :
        user = frappe.session.user
    roles = frappe.get_roles(user)
    
    if "Training Manager" in roles and not "System Manager" in roles:
        employee = frappe.get_doc("Employee",{"user_id":user})
        if employee:
            return """`tabTraining Schedule`.trainer = '{}' """.format(employee.name)
        