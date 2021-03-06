# Generated by Django 3.0.3 on 2020-07-23 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('usr_id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='用户ID')),
                ('usr_role', models.CharField(choices=[('M', '管理员'), ('T', '老师'), ('S', '学生')], max_length=1, verbose_name='用户角色')),
                ('usr_info', models.CharField(max_length=20, verbose_name='用户详细信息')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('coll_id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='学院编号')),
                ('coll_name', models.CharField(max_length=50, verbose_name='学院名称')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('cour_id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='课程编号')),
                ('cour_name', models.CharField(max_length=30, verbose_name='课程名称')),
                ('cour_major', models.CharField(max_length=20, verbose_name='课程专业')),
                ('cour_type', models.CharField(blank=True, max_length=10, verbose_name='课程类型')),
                ('cour_credit', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='课程学分')),
                ('cour_obj', models.CharField(blank=True, max_length=10, verbose_name='招生对象')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noti_title', models.CharField(max_length=100, verbose_name='通知标题')),
                ('noti_url', models.URLField(verbose_name='通知链接')),
                ('noti_from', models.CharField(max_length=30, verbose_name='通知单位')),
                ('noti_date', models.DateField(verbose_name='通知时间')),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_xn', models.CharField(max_length=10, verbose_name='学年')),
                ('rule_xq', models.CharField(max_length=2, verbose_name='学期')),
                ('rule_on', models.BooleanField(verbose_name='规则开关')),
                ('rule_begin_time', models.DateTimeField(verbose_name='开始时间')),
                ('rule_end_time', models.DateTimeField(verbose_name='结束时间')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='管理员工号')),
                ('admin_name', models.CharField(max_length=30, verbose_name='姓名')),
                ('admin_sex', models.CharField(choices=[('M', '男'), ('F', '女')], max_length=1, verbose_name='性别')),
                ('admin_credit', models.CharField(max_length=18, unique=True, verbose_name='身份证号')),
                ('admin_contact', models.CharField(max_length=30, verbose_name='联系方式')),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('spec_id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='专业编号')),
                ('spec_name', models.CharField(max_length=30, verbose_name='专业名称')),
                ('coll', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='spec', to='main.College', verbose_name='所属学院')),
            ],
        ),
        migrations.CreateModel(
            name='Arrangement',
            fields=[
                ('arr_id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='排课班号')),
                ('arr_capacity', models.IntegerField(verbose_name='选课容量')),
                ('arr_num', models.IntegerField(default=0, verbose_name='选课人数')),
                ('arr_loc', models.CharField(max_length=50, verbose_name='授课地点')),
                ('arr_time', models.CharField(max_length=255, verbose_name='时间安排')),
                ('arr_test', models.CharField(max_length=10, verbose_name='考试类型')),
                ('arr_test_time', models.CharField(blank=True, max_length=50, verbose_name='考试时间')),
                ('arr_remark', models.CharField(max_length=255, verbose_name='备注')),
                ('cour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arr', to='main.Course', verbose_name='课程编号')),
                ('spec', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arr', to='main.Speciality', verbose_name='专业编号')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teac', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='教室工号')),
                ('teac_name', models.CharField(max_length=30, verbose_name='教师姓名')),
                ('teac_credit', models.CharField(max_length=18, verbose_name='身份证号')),
                ('teac_sex', models.CharField(choices=[('M', '男'), ('F', '女')], max_length=1, verbose_name='性别')),
                ('teac_job', models.CharField(max_length=10, verbose_name='职称')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teac', to='main.Speciality', verbose_name='专业编号')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teac', to='main.College', verbose_name='所在单位')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('stu', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='学号')),
                ('stu_name', models.CharField(max_length=30, verbose_name='姓名')),
                ('stu_type', models.CharField(max_length=10, verbose_name='生源类型')),
                ('stu_grade', models.CharField(max_length=5, verbose_name='入学年份')),
                ('stu_credit', models.CharField(max_length=18, verbose_name='身份证号')),
                ('stu_class', models.CharField(max_length=10, verbose_name='班级')),
                ('coll', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stu', to='main.College', verbose_name='所在学院')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stu', to='main.Speciality', verbose_name='专业编号')),
            ],
        ),
        migrations.CreateModel(
            name='Choose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cho_time', models.DateTimeField(auto_now=True, verbose_name='抢课时间')),
                ('cho_score', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='成绩')),
                ('arr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cho', to='main.Arrangement', verbose_name='排课班号')),
                ('cour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cho', to='main.Course', verbose_name='课程编号')),
                ('stu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cho', to='main.Student', verbose_name='学生学号')),
            ],
        ),
        migrations.AddField(
            model_name='arrangement',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Teacher', verbose_name='任课教师'),
        ),
        migrations.AddConstraint(
            model_name='choose',
            constraint=models.UniqueConstraint(fields=('stu', 'cour'), name='unique_choosing'),
        ),
    ]
