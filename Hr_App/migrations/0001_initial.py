# Generated by Django 4.0.3 on 2023-12-15 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='announcement_images/')),
                ('image_path', models.FileField(blank=True, null=True, upload_to='announcement_images/')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicantJob',
            fields=[
                ('applicantjob_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('application_date', models.DateField()),
                ('status', models.CharField(max_length=255)),
                ('reason_for_hire', models.CharField(max_length=255)),
                ('cv', models.FileField(blank=True, null=True, upload_to='cvs/')),
            ],
        ),
        migrations.CreateModel(
            name='Applicants',
            fields=[
                ('applicant_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('mobile_number', models.DecimalField(decimal_places=0, max_digits=15)),
                ('dob', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Benefits',
            fields=[
                ('benefit_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('employee_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('join_date', models.DateField()),
                ('mobile_number', models.DecimalField(decimal_places=0, max_digits=15)),
                ('role', models.CharField(choices=[('employee', 'Employee'), ('hr_admin', 'HR Admin')], default='employee', max_length=10)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.department')),
            ],
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('job_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Leaves',
            fields=[
                ('leave_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('location_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('governorate', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Qualifications',
            fields=[
                ('qualification_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('degree', models.CharField(max_length=255)),
                ('institute', models.CharField(max_length=255)),
                ('graduation_year', models.CharField(max_length=4)),
                ('specialization', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('report_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('report_name', models.CharField(max_length=255)),
                ('report_type', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SalaryGrades',
            fields=[
                ('grade_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('salary_range', models.DecimalField(decimal_places=2, max_digits=10)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.jobs')),
            ],
        ),
        migrations.CreateModel(
            name='ReportDepartment',
            fields=[
                ('report_department_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.department')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.reports')),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceReview',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('review_date', models.DateField()),
                ('comments', models.TextField()),
                ('communication_skills', models.IntegerField(choices=[(1, 'Needs Improvement'), (2, 'Satisfactory'), (3, 'Exemplary')])),
                ('teamwork', models.IntegerField(choices=[(1, 'Requires Development'), (2, 'Effective'), (3, 'Highly Effective')])),
                ('problem_solving', models.IntegerField(choices=[(1, 'Limited'), (2, 'Adequate'), (3, 'Resourceful')])),
                ('adaptability', models.IntegerField(choices=[(1, 'Struggles to Adapt'), (2, 'Adapts Well'), (3, 'Quickly Adapts')])),
                ('punctuality', models.IntegerField(choices=[(1, 'Often Late'), (2, 'Usually On Time'), (3, 'Consistently On Time')])),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.employees')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to='Hr_App.employees')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveRecords',
            fields=[
                ('record_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('status', models.CharField(max_length=255)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.employees')),
                ('leave', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.leaves')),
            ],
        ),
        migrations.CreateModel(
            name='JobOpenings',
            fields=[
                ('opening_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('date_posted', models.DateField()),
                ('deadline', models.DateField()),
                ('description', models.CharField(max_length=1000)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.department')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.jobs')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationReview',
            fields=[
                ('review_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('score', models.DecimalField(decimal_places=2, max_digits=10)),
                ('review_date', models.DateField()),
                ('comments', models.CharField(max_length=255)),
                ('communication_skills', models.IntegerField(choices=[(1, 'Poor'), (2, 'Good'), (3, 'Excellent')])),
                ('facial_disclosure', models.IntegerField(choices=[(0, 'Hides expressions'), (1, 'Reveals expressions')])),
                ('eye_contact', models.IntegerField(choices=[(0, 'Doesn’t keep eye contact'), (1, 'Normal')])),
                ('posture', models.IntegerField(choices=[(0, 'Close'), (1, 'Open'), (2, 'Open all the time')])),
                ('self_control', models.IntegerField(choices=[(0, 'Not maintained'), (1, 'Maintained')])),
                ('personality', models.IntegerField(choices=[(1, 'Introvert'), (2, 'Ambivert'), (3, 'Extrovert')])),
                ('handling_question_1', models.IntegerField(choices=[(0, 'Poor'), (2, 'Good'), (3, 'Excellent')])),
                ('handling_question_2', models.IntegerField(choices=[(0, 'Poor'), (2, 'Good'), (3, 'Excellent')])),
                ('applicant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.applicants')),
                ('applicant_job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='Hr_App.applicantjob')),
            ],
        ),
        migrations.AddField(
            model_name='employees',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.jobs'),
        ),
        migrations.AddField(
            model_name='employees',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.locations'),
        ),
        migrations.AddField(
            model_name='employees',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='EmployeeQualification',
            fields=[
                ('employee_qualification_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.employees')),
                ('qualification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.qualifications')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('profile_picture', models.ImageField(upload_to='profile_pictures/')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.employees')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeePerformanceReview',
            fields=[
                ('performance_review_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.employees')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.performancereview')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeBenefits',
            fields=[
                ('employee_benefit_id', models.AutoField(max_length=255, primary_key=True, serialize=False)),
                ('benefit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.benefits')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.employees')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Hr_App.employees')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('messages', models.ManyToManyField(to='Hr_App.chatmessage')),
                ('participants', models.ManyToManyField(to='Hr_App.employees')),
            ],
        ),
        migrations.AddField(
            model_name='applicantjob',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_jobs', to='Hr_App.applicants'),
        ),
        migrations.AddField(
            model_name='applicantjob',
            name='opening',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='Hr_App.jobopenings'),
        ),
    ]
