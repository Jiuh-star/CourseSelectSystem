(function ($) {
    function changeUserForm() {
        const teacher = $('#teacher-group');
        const admin = $('#admin-group');
        const student = $('#student-group');
        switch ($('#id_usr_role').val()) {
            case "S":
                teacher.hide();
                admin.hide();
                student.show();
                break;
            case "T":
                student.hide();
                admin.hide();
                teacher.show();
                break;
            case "M":
                student.hide();
                teacher.hide();
                admin.show();
                break;
        }
    }

    $(function () {
        changeUserForm();
        $('#id_usr_role').change(changeUserForm);
    })
})(django.jQuery || $);