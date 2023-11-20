frappe.views.calendar['TS'] = {
    field_map: {
        start: 'start_date',
        end: 'end_date',
        id: 'training_schedule',
        allDay: 'all_day',
        title: 'course_and_trainer_name',
        status: 'course_name'

    },
    style_map: {
        Public: 'success',
        Private: 'info'
    }
}