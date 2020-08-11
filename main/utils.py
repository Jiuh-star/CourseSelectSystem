# -*- encoding: utf-8 -*-

# @File    :   utils.py
# @Time    :   2020/7/24 16:23
# @Software:   CourseChoosingSystem
# @Contact :   jiuh.star@gmail.com
from decimal import Decimal

from .models import (
    ADMIN, STUDENT, TEACHER, MALE, FEMALE,
    User,
)

MODEL_SEX_MAPPING = {
    MALE: '男',
    FEMALE: '女',
}


def get_grade_point(score, credit):
    if score is None:
        return ''
    if credit is None:
        raise RuntimeError("credit can't not be NoneType.")

    if score < 60:
        return 0

    score = Decimal(score)
    credit = Decimal(credit)

    gp = round(max(score / 10 - 5, 0) * credit, 2)

    return gp


def generate_courses_children(course_names, url, method='GET', start_func='null', end_func='null'):
    return ({
        'courseName': arr['cour__cour_name'],
        'href': f"javascript:loadXMLDoc('{url}?arrangementId={arr['arr_id']}','{method}','',{start_func},{end_func});"
    } for arr in course_names)


def cleanup_user_model(student_model, teacher_model, admin_model, needed=(STUDENT, TEACHER, ADMIN)):
    if STUDENT in needed:
        yield from ({
            'userId': user['usr_id'],
            'username': user['student__stu_name'],
            'group': '学生',
            'sex': '',
            'college': user['student__coll__coll_name'],
            'speciality': user['student__spec__spec_name'],
        } for user in student_model)
    elif TEACHER in needed:
        yield from ({
            'userId': user['usr_id'],
            'username': user['teacher__teac_name'],
            'group': '教师',
            'sex': MODEL_SEX_MAPPING[user['teacher__teac_sex']],
            'college': user['teacher__unit__coll_name'],
            'speciality': user['teacher__spec__spec_name'],
        } for user in teacher_model)
    elif ADMIN in needed:
        yield from ({
            'userId': user['usr_id'],
            'username': user['admin__admin_name'],
            'group': '管理员',
            'sex': MODEL_SEX_MAPPING[user['admin__admin_sex']],
            'college': '',
            'speciality': '',
        } for user in admin_model)


def get_user_info(user_id):
    base_user_info = User.objects.values('usr_id', 'usr_role', 'last_login',

                                         'student__stu_name', 'student__stu_type', 'student__stu_credit',
                                         'student__stu_grade',
                                         'student__stu_class', 'student__coll__coll_name', 'student__spec__spec_name',

                                         'teacher__teac_name', 'teacher__teac_job', 'teacher__teac_credit',
                                         'teacher__unit__coll_name', 'teacher__spec__spec_name',

                                         'admin__admin_name', 'admin__admin_sex', 'admin__admin_credit',
                                         'admin__admin_contact').get(user_id=user_id)
    detail = None
    if base_user_info['usr_id'] == STUDENT:
        # detail =
        # TODO: display infos.
        pass
    elif base_user_info['usr_id'] == TEACHER:
        pass
    elif base_user_info['usr_id'] == ADMIN:
        pass

    return base_user_info, detail
