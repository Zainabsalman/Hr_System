from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


# Create your models here.
from django.db import models

# class User(models.Model):
#     id = models.AutoField(primary_key=True, max_length=255)
#     username=models.CharField(max_length=255)
#     password1=models.CharField(max_length=255)
#     password2= models.CharField(max_length=255)

class Jobs(models.Model):
    job_id = models.AutoField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name 

class Locations(models.Model):
    location_id = models.AutoField(primary_key=True, max_length=255)
    country = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    governorate = models.CharField(max_length=255)

    def __str__(self):
        return self.country
    def __str__(self):
        return self.city

class Department(models.Model):
    department_id = models.AutoField(primary_key=True, max_length=255)
    department_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.department_name  

class Employees(models.Model):
    employee_id = models.AutoField(primary_key=True, max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    email = models.EmailField(max_length = 254)
    join_date = models.DateField()
    mobile_number = models.DecimalField(max_digits=15, decimal_places=0)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('employee', 'Employee'), ('hr_admin', 'HR Admin')], default='employee')


    def __str__(self):
        return self.name


class EmployeeProfile(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/')

    def __str__(self):
        return self.employee.name


class ChatMessage(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.user.username} at {self.timestamp}"

class Chat(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(Employees)
    messages = models.ManyToManyField(ChatMessage)

    def __str__(self):
        return self.name

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='announcement_images/', null=True, blank=True)
    image_path = models.FileField(upload_to='announcement_images/', null=True, blank=True) 
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.title


class PerformanceReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey('Employees', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('Employees', related_name='reviewer', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    review_date = models.DateField()
    comments = models.TextField()
    communication_skills = models.IntegerField(choices=[(1, 'Needs Improvement'), (2, 'Satisfactory'), (3, 'Exemplary')])
    teamwork = models.IntegerField(choices=[(1, 'Requires Development'), (2, 'Effective'), (3, 'Highly Effective')])
    problem_solving = models.IntegerField(choices=[(1, 'Limited'), (2, 'Adequate'), (3, 'Resourceful')])
    adaptability = models.IntegerField(choices=[(1, 'Struggles to Adapt'), (2, 'Adapts Well'), (3, 'Quickly Adapts')])
    punctuality = models.IntegerField(choices=[(1, 'Often Late'), (2, 'Usually On Time'), (3, 'Consistently On Time')])
    leadership = models.IntegerField(choices=[(1, 'Occasionally Demonstrated'), (2, 'Frequently Demonstrated'), (3, 'Consistently Demonstrated')])
    # Other relevant fields as needed

    def __str__(self):
        return f"Performance Review for {self.employee} on {self.review_date}"


class EmployeePerformanceReview(models.Model):
    performance_review_id = models.AutoField(primary_key=True, max_length=255)
    review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee
    
class Qualifications(models.Model):
    qualification_id = models.AutoField(primary_key=True, max_length=255)
    degree = models.CharField(max_length=255)
    institute = models.CharField(max_length=255)
    graduation_year = models.CharField(max_length=4)
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return self.degree



class Benefits(models.Model):
    benefit_id = models.AutoField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class SalaryGrades(models.Model):
    grade_id = models.AutoField(primary_key=True, max_length=255)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    salary_range = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.job

class Reports(models.Model):
    report_id = models.AutoField(primary_key=True, max_length=255)
    report_name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=255)
    date = models.DateField()
    description = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.report_name

class Leaves(models.Model):
    leave_id = models.AutoField(primary_key=True, max_length=255)
    type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class EmployeeLeave(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    leave = models.ForeignKey(Leaves, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=100, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"{self.employee.name} - {self.leave.type}"


class Applicants(models.Model):
    applicant_id = models.AutoField(primary_key=True, max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    mobile_number = models.DecimalField(max_digits=15, decimal_places=0)
    dob = models.DateField()
    email = models.EmailField()
     
    def __str__(self):
        return self.name
class JobOpenings(models.Model):
    opening_id = models.AutoField(primary_key=True, max_length=255)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_posted = models.DateField()
    deadline = models.DateField()
    description = models.CharField( max_length=1000)

    @property
    def job_name(self):
        return self.job.name
    
    @property
    def job_description(self):
        return self.job.description

    @property
    def department_name(self):
        return self.department.department_name
    
    def __str__(self):
        return self.job    
class ApplicantJob(models.Model):
    applicantjob_id = models.AutoField(primary_key=True, max_length=255)
    applicant = models.ForeignKey(Applicants, on_delete=models.CASCADE, related_name='applied_jobs')
    opening = models.ForeignKey(JobOpenings, on_delete=models.CASCADE, related_name='applicants')
    application_date = models.DateField()
    status = models.CharField(max_length=255)
    reason_for_hire = models.CharField(max_length=255)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)

    def __str__(self):
        return str(self.applicant)

class EvaluationReview(models.Model):
    review_id = models.AutoField(primary_key=True, max_length=255)
    score = models.DecimalField(max_digits=10, decimal_places=2)
    review_date = models.DateField()
    applicant_id = models.ForeignKey(Applicants, on_delete=models.CASCADE)
    comments = models.CharField(max_length=255)
    communication_skills = models.IntegerField(choices=[(1, 'Poor'), (2, 'Good'), (3, 'Excellent')])
    facial_disclosure = models.IntegerField(choices=[(0, 'Hides expressions'), (1, 'Reveals expressions')])
    eye_contact = models.IntegerField(choices=[(0, 'Doesn’t keep eye contact'), (1, 'Normal')])
    posture = models.IntegerField(choices=[(0, 'Close'), (1, 'Open'), (2, 'Open all the time')])
    self_control = models.IntegerField(choices=[(0, 'Not maintained'), (1, 'Maintained')])
    personality = models.IntegerField(choices=[(1, 'Introvert'), (2, 'Ambivert'), (3, 'Extrovert')])
    handling_question_1 = models.IntegerField(choices=[(0, 'Poor'), (2, 'Good'), (3, 'Excellent')])
    handling_question_2 = models.IntegerField(choices=[(0, 'Poor'), (2, 'Good'), (3, 'Excellent')])
    applicant_job = models.ForeignKey(ApplicantJob, on_delete=models.CASCADE, related_name='evaluations', blank=True, null=True)

    def total_score(self):
        # Calculate total score based on all these fields
        total = sum([
            self.communication_skills,
            self.facial_disclosure,
            self.eye_contact,
            self.posture,
            self.self_control,
            self.personality,
            self.handling_question_1,
            self.handling_question_2,
            # ... add the rest of the handling question fields here ...
        ])
        return total

    def __str__(self):
        return f"Review for {self.applicant_id.name} on {self.review_date}"



class ReportDepartment(models.Model):
    report_department_id = models.AutoField(primary_key=True, max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)

    def __str__(self):
        return self.department




class EmployeeQualification(models.Model):
    employee_qualification_id = models.AutoField(primary_key=True, max_length=255)
    qualification = models.ForeignKey(Qualifications, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee
    

class LeaveRecords(models.Model):
    record_id = models.AutoField(primary_key=True, max_length=255)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    leave = models.ForeignKey(Leaves, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.employee
    

class EmployeeBenefits(models.Model):
    employee_benefit_id = models.AutoField(primary_key=True, max_length=255)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    benefit = models.ForeignKey(Benefits, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee
    

#class Person(models.Model):
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
    # email = models.EmailField(max_length=254)

#how to use an instance of ur object 
#person = Person(first_name='John', last_name='Doe', email='john.doe@example.com')
#person.save()

