from datetime import datetime

from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from . import models
from .utils import get_grade_point, generate_courses_children

TEACHER = '教师'
STUDENT = '学生'
ADMIN = '管理员'

MODEL_ROLES_MAPPING = {
    models.TEACHER: TEACHER,
    models.STUDENT: STUDENT,
    models.ADMIN: ADMIN,
}
COMMON_MENU = (
    {'title': '通知公告', 'href': "javascript:loadXMLDoc('./notification');", 'icon': 'fas fa-tachometer-alt'},
)
STUDENT_MENU = (
    {'title': '学生选课',
     'href': "javascript:loadXMLDoc('./stu/selection','GET','',null,loadSearchFunc)",
     'icon': 'fas fa-table'},
    {'title': '开课信息',
     'href': "javascript:loadXMLDoc('./stu/all-courses');",
     'icon': 'fas fa-search'},
    {'title': '已选课程',
     'href': "javascript:loadXMLDoc('./stu/my-courses','GET','',null,flashBarColor);",
     'icon': 'fas fa-user-check'},
)
ALL_COURSES_TABLE_FIELDS = ('cour_id', 'arr_id', 'cour__cour_name', 'arr_capacity', 'teacher__teac_name',
                            'spec__spec_name', 'cour__cour_credit', 'arr_loc', 'arr_time', 'arr_test',
                            'cour__cour_obj', 'arr_remark')


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'captcha/text_field.html'


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control form-control-user", "placeholder": "用户名"}
    ), max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control form-control-user", "placeholder": "密码"}
    ), max_length=20)
    captcha = CaptchaField(widget=CustomCaptchaTextInput(
        attrs={"class": "form-control form-control-user", "placeholder": "验证码"}
    ))


def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)


def forbidden(request, exception=None):
    return render(request, '403.html', status=403)


def log_in(request):
    if request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)

                # 管理员登录
                if user.is_staff:
                    return redirect(reverse('admin:login'))

                return redirect(reverse('main-view'))
            else:
                # 登录失败
                form.add_error('username', '用户名或密码错误！')
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form})


@login_required
def main_view(request):
    role = MODEL_ROLES_MAPPING[request.user.usr_role]
    username = None
    menu = None
    if role == STUDENT:
        username = request.user.student.stu_name
        menu = COMMON_MENU + STUDENT_MENU
    elif role == TEACHER:
        username = request.user.teacher.teac_name
        course_names = models.Arrangement.objects.values(
            'arr_id', 'cour__cour_name'
        ).filter(teacher_id=request.user.usr_id)
        menu = COMMON_MENU + (
            {
                'title': '任教课程',
                'control': 'collapse-1',
                'icon': 'fas fa-table',
                'child': generate_courses_children(course_names, url=reverse('teach-courses'), end_func='loadChart')
            },
            {
                'title': '成绩管理',
                'control': 'collapse-2',
                'icon': 'fas fa-poll',
                'child': generate_courses_children(course_names, url=reverse('scores'))
            }
        )

    return render(request, 'main/index.html', {'role': role, 'username': username, 'menu': menu})


@login_required
def notification_table(request):
    page = request.GET.get('page', '1')[:10]
    limit = request.GET.get('limit', '10')[:10]

    paginator = Paginator(models.Notification.objects.all().order_by('-noti_date'), limit)
    page_obj = paginator.get_page(page)

    return render(request, 'main/notification.html', context={'page_obj': page_obj, 'limit': limit})


@login_required()
@permission_required('main.student_access', raise_exception=True)
def all_courses_table(request):
    arrangements = None
    units = models.College.objects.all()

    post_params = {}
    if request.POST:
        post_params = {
            'collegeId': request.POST.get('collegeId', ''),
            'courseName': request.POST.get('courseName', ''),
            'courseId': request.POST.get('courseId', ''),
            'arrangementId': request.POST.get('arrangementId', ''),
            'obj': request.POST.get('obj', ''),
            'teacherName': request.POST.get('teacherName', ''),
        }

        arrangements = models.Arrangement.objects.values(*ALL_COURSES_TABLE_FIELDS).filter(
            spec__coll__coll_id__icontains=post_params['collegeId'],
            cour__cour_name__icontains=post_params['courseName'],
            cour__cour_id__icontains=post_params['courseId'],
            arr_id__icontains=post_params['arrangementId'],
            cour__cour_obj__icontains=post_params['obj'],
            teacher__teac_name__icontains=post_params['teacherName'],
        )

    return render(request, 'main/all-courses.html',
                  {'units': units, 'arrangements': arrangements,
                   'params': post_params,
                   'request_method': request.method})


@login_required
@permission_required('main.student_access', raise_exception=True)
def selection(request):
    limit = request.GET.get('limit', '10')[:10]
    page = request.GET.get('page', '1')[:10]
    query = request.GET.get('q', '')[:20]

    try:
        now = datetime.now()
        rule = models.Rule.objects.get(rule_on=True, rule_begin_time__lte=now, rule_end_time__gte=now)
        error = ''
        title = '{}学年度{}学期选课'.format(rule.rule_xn, rule.rule_xq)
    except models.Rule.DoesNotExist:
        error = '系统已经关闭'
        title = ''

    paginator = Paginator(models.Arrangement.objects.prefetch_related('cour', 'teacher')
                          .filter(arr_id__exact=query), limit) \
        if query \
        else Paginator(models.Arrangement.objects.prefetch_related('cour', 'teacher').all(), limit)

    page_obj = paginator.get_page(page)

    return render(request, 'main/selection.html',
                  {'error': error, 'title': title, 'page_obj': page_obj, 'limit': limit})


@login_required
@permission_required('main.student_access', raise_exception=True)
def my_courses_table(request):
    stu_id = request.user.usr_id

    history_model = models.Choose.objects.filter(stu_id=stu_id).values(
        'arr_id', 'arr__arr_time', 'arr__teacher__teac_name', 'arr__arr_loc',
        'cour_id', 'cour__cour_name', 'cour__cour_type', 'cour__cour_credit',
        'cho_score',
    )
    history = []
    for h in history_model:
        history.append({
            'courseId': h['cour_id'],
            'courseName': h['cour__cour_name'],
            'score': h['cho_score'] or '',
            'courseType': h['cour__cour_type'],
            'courseCredit': h['cour__cour_credit'],
            'gradePoint': get_grade_point(h['cho_score'], h['cour__cour_credit'])
        })

    on_rules = models.Rule.objects.filter(rule_on=True)
    q = Q()
    for rule in on_rules:
        q &= Q(cho_time__range=(rule.rule_begin_time, rule.rule_end_time))
    my_courses = history_model.filter(q)

    return render(request, 'main/my-courses.html', {'mine': my_courses, 'history': history})


@login_required
@permission_required('main.student_access', raise_exception=True)
def select_course(request):
    if request.method == 'GET':
        return HttpResponseForbidden()

    is_remove = request.POST.get('isRemove', '')
    arr_id = request.POST['arrangementId']

    try:
        arr = models.Arrangement.objects.get(
            arr_id__exact=arr_id,
            arr_capacity__gt=F('arr_num'),
        )
        arr.arr_num = F('arr_num') + (-1 if is_remove else 1)

        if is_remove:
            models.Choose.objects.get(
                arr_id__exact=arr_id,
                stu_id=request.user.usr_id,
            ).delete()
        else:
            models.Choose.objects.create(
                arr_id=arr_id,
                cour_id=arr.cour_id,
                stu_id=request.user.usr_id,
            )

        arr.save(update_fields=('arr_num',))

    except (models.Arrangement.DoesNotExist, KeyError):
        return HttpResponseForbidden('{}失败，请刷新重试！'.format('退课' if is_remove else '选课'))
    except IntegrityError:
        return HttpResponseForbidden('该课程已选，请勿重复选课！')

    return HttpResponse('成功！')


@login_required
@permission_required('main.teacher_access', raise_exception=True)
def teach_courses_table(request):
    try:
        arr_id = request.GET['arrangementId']
        arr = models.Arrangement.objects.get(arr_id=arr_id)
        arr_major = arr.spec.spec_name if arr.spec else ''
        chart_data = {
            '内招生': models.Choose.objects.filter(arr_id=arr_id, stu__stu_type__icontains='内招生').count(),
            '外招生': models.Choose.objects.filter(arr_id=arr_id, stu__stu_type__icontains='外招生').count(),
        }
    except (KeyError, models.Arrangement.DoesNotExist):
        return HttpResponseForbidden()

    return render(request, 'main/teach-course.html',
                  {'arr': arr, 'arr_major': arr_major, 'chart_data': chart_data}
                  )


@login_required
@permission_required('main.teacher_access', raise_exception=True)
def scores(request):
    try:
        arr_id = request.GET['arrangementId']
        arr = models.Arrangement.objects.get(arr_id=arr_id)

        title = arr.cour.cour_name
        stu_infos = []
        for cho in models.Choose.objects.prefetch_related('stu', 'stu__spec').filter(arr_id=arr_id):
            stu_infos.append({
                'stuId': cho.stu_id,
                'stuName': cho.stu.stu_name,
                'stuSpec': cho.stu.spec.spec_name,
                'stuScore': cho.cho_score
            })
    except (KeyError, models.Arrangement.DoesNotExist):
        return HttpResponseForbidden()

    return render(request, 'main/score-manage.html',
                  {'arrId': arr_id, 'title': title, 'infos': stu_infos})


@login_required
@permission_required('main.teacher_access', raise_exception=True)
def save_scores(request):
    try:
        arr_id = request.POST.get('arrId')

        for stu_id, score in request.POST.items():
            if stu_id == 'arrId' or stu_id == 'csrfmiddlewaretoken':
                continue

            if not 0 <= int(score) <= 100:
                raise ValueError
            cho = models.Choose.objects.get(stu_id=stu_id, arr_id=arr_id)
            cho.cho_score = score if not cho.cho_score else cho.cho_score
            cho.save(update_fields=('cho_score',))

    except KeyError:
        return HttpResponseForbidden()
    except (models.Choose.DoesNotExist, ValueError):
        return HttpResponseBadRequest()

    return HttpResponse('提交成功')
