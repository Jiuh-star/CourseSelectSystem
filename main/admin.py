from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group

from . import models


class StudentInline(admin.StackedInline):
    model = models.Student
    verbose_name = '学生'


class TeacherInline(admin.StackedInline):
    model = models.Teacher
    verbose_name = '教师'


class AdminInline(admin.StackedInline):
    model = models.Admin
    verbose_name = '管理员'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': '重写以覆盖'}
    ), max_length=20, required=False)

    class Meta:
        model = models.User
        exclude = ('password',)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('usr_id', 'usr_role', 'usr_info')
    inlines = (StudentInline, TeacherInline, AdminInline)
    exclude = ('password',)
    form = UserForm
    readonly_fields = ('last_login',)
    search_fields = ('usr_id',)
    list_filter = ('usr_role',)

    class Media:
        js = ('js/admin.js',)

    def save_model(self, request, obj, form, change):
        password = request.POST.get('password')
        if password:
            obj.set_password(password)

        obj.save()


@admin.register(models.College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('coll_id', 'coll_name')


@admin.register(models.Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('spec_id', 'spec_name', 'coll')


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('cour_id', 'cour_name', 'cour_type', 'cour_major', 'cour_credit', 'cour_obj')
    list_filter = ('cour_type', 'cour_obj', 'cour_major')
    search_fields = ('cour_id', 'cour_name')


@admin.register(models.Arrangement)
class ArrangementAdmin(admin.ModelAdmin):
    list_display = ('arr_id', 'cour', 'spec', 'teacher', 'arr_remark')
    list_filter = ('spec', 'teacher')
    search_fields = (
        'arr_id', 'cour__cour_name', 'cour__cour_id',
        'spec__spec_name', 'spec__spec_id',
        'teacher__teac__usr_id', 'teacher__teac_name',
    )


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    date_hierarchy = 'noti_date'
    list_display = ('noti_title', 'noti_date', 'noti_from')
    list_filter = ('noti_from',)


@admin.register(models.Choose)
class ChooseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'stu', 'cho_time', 'cho_score')
    search_fields = (
        'stu__stu__usr_id', 'stu__stu_name',
        'cour__cour_id', 'cour__cour_name', 'arr__arr_id',
    )
    list_editable = ('cho_score',)
    autocomplete_fields = ('cour', 'arr')


@admin.register(models.Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'rule_begin_time', 'rule_end_time', 'rule_on')
    list_filter = ('rule_xn', 'rule_on')


admin.site.unregister(Group)
