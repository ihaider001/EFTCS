console.log("%%%%%%%%%%%%%%%%%  start   %%%%%%%%%%%  training schedule calender calender view")
var text1 = "Hello";
var text2 = "world!";
var result = text1.concat(" ", text2);
console.log("TTTTTTTTTTTTTTTT00",result)
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

console.log("%%%%%%%%%%%%%%%%%  End   %%%%%%%%%%%  training schedule calender calender view")