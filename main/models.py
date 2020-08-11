from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

STUDENT = 'S'
TEACHER = 'T'
ADMIN = 'M'

MALE = 'M'
FEMALE = 'F'

SEX_CHOICES = ((MALE, '男'), (FEMALE, '女'))
ROLES_CHOICES = ((ADMIN, '管理员'), (TEACHER, '教师'), (STUDENT, '学生'))


class College(models.Model):
    """
    学院信息表\n
    字段说明：\n
    coll_id - 学院编号(PK)\n
    coll_name - 学院名称\n
    """
    coll_id = models.CharField(max_length=20, primary_key=True, verbose_name='学院编号')
    coll_name = models.CharField(max_length=50, verbose_name='学院名称')

    def __str__(self):
        return '{}({})'.format(self.coll_name, self.pk)


class Speciality(models.Model):
    """
    专业信息表\n
    字段说明：\n
    spec_id - 专业编号(PK)\n
    spec_name - 专业名称\n
    spec_coll - 所属学院(FK)\n
    """
    spec_id = models.CharField(max_length=20, primary_key=True, verbose_name='专业编号')
    spec_name = models.CharField(max_length=30, verbose_name='专业名称')
    coll = models.ForeignKey(College, on_delete=models.PROTECT, related_name='spec', verbose_name='所属学院')

    def __str__(self):
        return '{}({})'.format(self.spec_name, self.pk)


class Course(models.Model):
    """
    课程基本信息表\n
    字段说明：\n
    cour_id - 课程编号(PK)\n
    cour_name - 课程名称\n
    cour_major - 课程专业\n
    cour_type - 课程类型\n
    cour_credit - 课程学分\n
    cour_obj - 招生对象\n
    """
    cour_id = models.CharField(max_length=20, primary_key=True, verbose_name='课程编号')
    cour_name = models.CharField(max_length=30, verbose_name='课程名称')
    cour_major = models.CharField(max_length=20, verbose_name='课程专业')
    cour_type = models.CharField(max_length=10, blank=True, verbose_name='课程类型')
    cour_credit = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='课程学分')
    cour_obj = models.CharField(max_length=10, blank=True, verbose_name='招生对象')

    def __str__(self):
        return '{}({})'.format(self.cour_name, self.pk)


class MainUserManager(BaseUserManager):
    def create_user(self, usr_id, password, usr_info, usr_role='S', **other_fields):
        if not usr_id:
            raise ValueError('The given username must be set')
        usr_id = self.model.normalize_username(usr_id)
        user = self.model(usr_id=usr_id, usr_info=usr_info, usr_role=usr_role, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usr_id, password, usr_info, usr_role='M', **other_fields):
        self.create_user(usr_id, password, usr_info, 'M', **other_fields)


class User(AbstractBaseUser):
    """
    用户信息表\n
    字段说明：\n
    usr_id - 用户账号(PK)\n
    usr_role - 用户角色\n
    password - 用户密码\n
    usr_info - 用户信息(FK)\n
    """
    objects = MainUserManager()
    usr_id = models.CharField(max_length=20, primary_key=True, unique=True, verbose_name='用户ID')
    usr_role = models.CharField(max_length=1, choices=ROLES_CHOICES, verbose_name='用户角色')
    usr_info = models.CharField(max_length=20, verbose_name='用户详细信息')

    USERNAME_FIELD = 'usr_id'
    REQUIRED_FIELDS = ['usr_role', 'usr_info']

    def has_perm(self, perm, obj=None):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        return self.has_perms(perms, obj)

    def has_perms(self, perm, obj=None):

        if obj:
            return obj.has_perms()
        if 'main.student_access' in perm and self.usr_role == STUDENT:
            return True
        elif 'main.teacher_access' in perm and self.usr_role == TEACHER:
            return True
        # elif 'main.admin_access' in perm and self.usr_role == ADMIN:
        elif self.usr_role == ADMIN:
            return True
        return False

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usr_role == ADMIN


class Teacher(models.Model):
    """
    教室基本信息表\n
    字段说明：\n
    teac_id - 工号(PK)\n
    teac_name - 姓名\n
    teac_credit - 身份证号\n
    teac_sex - 性别\n
    teac_job - 教师职称\n
    unit - 所在单位(FK)\n
    spec - 专业(FK)\n
    """
    teac = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='教室工号')
    teac_name = models.CharField(max_length=30, verbose_name='教师姓名')
    teac_credit = models.CharField(max_length=18, verbose_name='身份证号')
    teac_sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name='性别')
    teac_job = models.CharField(max_length=10, verbose_name='职称')
    unit = models.ForeignKey(College, on_delete=models.PROTECT, related_name='teac', verbose_name='所在单位')
    spec = models.ForeignKey(Speciality, on_delete=models.PROTECT, related_name='teac', verbose_name='专业编号')

    def __str__(self):
        return '{}({})'.format(self.teac_name, self.pk)


class Student(models.Model):
    """
    学生基本信息表\n
    字段说明：\n
    stu_id - 学号(PK)\n
    stu_name - 姓名\n
    stu_type - 内外招生\n
    stu_grade - 年级\n
    stu_credit - 身份证号\n
    stu_class - 班级\n
    coll - 所在学院(FK)\n
    spec - 专业(FK)\n
    """
    stu = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='学号')
    stu_name = models.CharField(max_length=30, verbose_name='姓名')
    stu_type = models.CharField(max_length=10, verbose_name='生源类型')
    stu_grade = models.CharField(max_length=5, verbose_name='入学年份')
    stu_credit = models.CharField(max_length=18, verbose_name='身份证号')
    stu_class = models.CharField(max_length=10, verbose_name='班级')
    coll = models.ForeignKey(College, on_delete=models.PROTECT, related_name='stu', verbose_name='所在学院')
    spec = models.ForeignKey(Speciality, on_delete=models.PROTECT, related_name='stu', verbose_name='专业编号')

    def __str__(self):
        return '{}({})'.format(self.stu_name, self.pk)


class Arrangement(models.Model):
    """
    课程排课信息表\n
    字段说明：\n
    arr_id - 排课班号(PK)\n
    arr_capacity - 课程容量\n
    arr_num - 选课人数\n
    arr_loc - 授课地点\n
    arr_time - 时间安排\n
    arr_test - 考试类型\n
    arr_test_time - 考试时间\n
    arr_remark - 备注\n
    teacher - 任课教师(FK)\n
    cour - 课程编号(FK)\n
    spec - 专业编号(FK)\n
    """
    arr_id = models.CharField(max_length=20, primary_key=True, verbose_name='排课班号')
    arr_capacity = models.IntegerField(verbose_name='选课容量')
    arr_num = models.IntegerField(default=0, verbose_name='选课人数')
    arr_loc = models.CharField(max_length=50, verbose_name='授课地点')
    arr_time = models.CharField(max_length=255, verbose_name='时间安排')
    arr_test = models.CharField(max_length=10, verbose_name='考试类型')
    arr_test_time = models.CharField(max_length=50, blank=True, verbose_name='考试时间')
    arr_remark = models.CharField(max_length=255, verbose_name='备注')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='任课教师')
    cour = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='arr', verbose_name='课程编号')
    spec = models.ForeignKey(Speciality, on_delete=models.CASCADE, related_name='arr', null=True, blank=True,
                             verbose_name='专业编号')

    def __str__(self):
        return '{}(排课：{})'.format(self.cour.cour_name, self.pk)


class Choose(models.Model):
    """
    学生抢课登记表\n
    字段说明：\n
    id - 自增主键\n
    cho_time - 抢课时间\n
    cho_score - 成绩\n
    stu - 学生学号(FK)\n
    arr - 排课班号(FK)\n
    cour - 排课班号(FK)\n
    """
    cho_time = models.DateTimeField(auto_now=True, verbose_name='抢课时间')
    cho_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='成绩')
    stu = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='cho', verbose_name='学生学号')
    arr = models.ForeignKey(Arrangement, on_delete=models.CASCADE, related_name='cho', verbose_name='排课班号')
    cour = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cho', verbose_name='课程编号')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stu', 'cour'], name='unique_choosing')
        ]

    def __str__(self):
        return '{}:{}({})'.format(self.stu.stu_name, self.cour.cour_name, self.arr_id)


class Admin(models.Model):
    """
    管理员基本信息表\n
    字段说明：\n
    admin_id - 工号(PK)\n
    admin_name - 姓名\n
    admin_sex - 性别\n
    admin_credit - 身份证号\n
    admin_contact - 联系方式\n
    """
    admin = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='管理员工号')
    admin_name = models.CharField(max_length=30, verbose_name='姓名')
    admin_sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name='性别')
    admin_credit = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    admin_contact = models.CharField(max_length=30, verbose_name='联系方式')

    def __str__(self):
        return '{}({})'.format(self.admin_name, self.pk)


class Notification(models.Model):
    """
    通知公告表\n
    字段说明：\n
    noti_title - 通知标题\n
    noti_url - 通知链接\n
    noti_from - 通知单位\n
    noti_date - 通知时间\n
    """
    noti_title = models.CharField(max_length=100, verbose_name='通知标题')
    noti_url = models.URLField(verbose_name='通知链接')
    noti_from = models.CharField(max_length=30, verbose_name='通知单位')
    noti_date = models.DateField(verbose_name='通知时间')

    def __str__(self):
        return self.noti_title


class Rule(models.Model):
    """
    选课规则表\n
    字段说明：\n
    rule_xn - 学年\n
    rule_sq - 学期\n
    rule_on - 规则开关\n
    rule_begin_time - 开始时间\n
    rule_end_time - 结束时间\n
    """
    rule_xn = models.CharField(max_length=10, verbose_name='学年')
    rule_xq = models.CharField(max_length=2, verbose_name='学期')
    rule_on = models.BooleanField(verbose_name='规则开关')
    rule_begin_time = models.DateTimeField(verbose_name='开始时间')
    rule_end_time = models.DateTimeField(verbose_name='结束时间')

    def __str__(self):
        return '{}学年第{}学期选课'.format(self.rule_xn, self.rule_xq)
