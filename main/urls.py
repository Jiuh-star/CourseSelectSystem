from django.urls import path

from . import views

urlpatterns = [
    # path('teacher', views.teacher, name='teacher'),
    # path('student', views.student, name='student'),
    path('main-view', views.main_view, name='main-view'),
    # 通用信息
    path('notification', views.notification_table, name='notification'),
    # student's info
    path('stu/my-courses', views.my_courses_table, name='my-courses'),
    path('stu/all-courses', views.all_courses_table, name='all-courses'),
    path('stu/selection', views.selection, name='selection'),
    path('stu/select-course', views.select_course, name='select-course'),
    # teacher's info
    path('teac/teach-courses', views.teach_courses_table, name='teach-courses'),
    path('teac/scores', views.scores, name='scores'),
    path('teac/save-scores', views.save_scores, name='save-scores'),
    # admin's views
    # user manager
    # path('admin/user-manage', views.user_manage, name='all-users'),
    # path('admin/modal/user-info', views.user_info, name='user-info'),
    # path('admin/create-user', views.create_user, name='create-user'),
    # courses & arrangements
    # path('admin/all-courses', views.admin_all_courses_table, name='admin-all-courses'),
    # path('admin/arrangements', views.arrangements, name='arrangements'),
    # # selection rules
    # path('admin/rules', views.rules, name='rules'),
    # 登录窗体
    path('', views.log_in, name='login')
]

handler404 = views.page_not_found
handler403 = views.forbidden
