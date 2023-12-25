from datetime import timezone
import os
from django.utils import timezone
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from pymongo import MongoClient
from .models import Announcement, ApplicantJob, Applicants, EmployeeLeave, Employees, EvaluationReview, JobOpenings, Announcement,LeaveRecords, Leaves
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .functions import calculate_leave_days, get_user_role, handle_uploaded_file, handle_uploaded_file2
from django.core.serializers.json import DjangoJSONEncoder


from .forms import (
    
    AnnouncementForm,
    ApplicantForm,
    EmployeeForm,
    EmployeeLeaveForm,
    PerformanceReviewForm,
    VacancyForm,
    ApplicantJobForm,
    
    
)
import logging

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from calendar import monthrange

# Create your views here.

#def index(request):
 #   return HttpResponse("Hello World")

 #   from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Applicants, Employees  # Make sure to import your models

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check if the user is an Applicant
            if Applicants.objects.filter(user=user).exists():
                return redirect('applicant_dashboard')

            # Check if the user is an Employee and its role
            elif Employees.objects.filter(user=user).exists():
                employee = Employees.objects.get(user=user)
                if employee.role == 'hr_admin':
                    return redirect('/')
                else:
                    return redirect('employee_dashboard')  # Redirect to employee dashboard

            # Fallback redirect if user is neither an Applicant nor an Employee
            return redirect('login')  # Redirect to a default or home page

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'logIn.html')

from django.db.models import Count
from django.utils import timezone
import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Applicants, JobOpenings, Employees, Announcement, LeaveRecords, ApplicantJob  # Import your models
import json
from django.core.serializers.json import DjangoJSONEncoder


@login_required
def index(request):
    today = timezone.now()
    current_year, current_month = today.year, today.month

    # Calculate the first day of the current month
    first_day_current_month = datetime.date(current_year, current_month, 1)

    # Calculate the first day of the next month
    if current_month == 12:
        first_day_next_month = datetime.date(current_year + 1, 1, 1)
    else:
        first_day_next_month = datetime.date(current_year, current_month + 1, 1)

    # Last day of the current month is one day before the first day of the next month
    last_day_current_month = first_day_next_month - datetime.timedelta(days=1)

    # Calculate the first and last day of the last month
    first_day_last_month = first_day_current_month - datetime.timedelta(days=monthrange(current_year, current_month - 1)[1])
    last_day_last_month = first_day_current_month - datetime.timedelta(days=1)

    # Aggregate data for the current month
    current_month_data = ApplicantJob.objects.filter(
        application_date__range=[first_day_current_month, last_day_current_month]
    ).values('opening__job__name').annotate(
        total_applications=Count('applicantjob_id')
    ).order_by('-total_applications')[:5]  # Top 5 jobs

    # Aggregate data for the last month
    last_month_data = ApplicantJob.objects.filter(
        application_date__range=[first_day_last_month, last_day_last_month]
    ).values('opening__job__name').annotate(
        total_applications=Count('applicantjob_id')
    ).order_by('-total_applications')[:5]  # Top 5 jobs

    # Other context data
    applicants = Applicants.objects.all()
    job_openings = JobOpenings.objects.all()
    all_employees = Employees.objects.all()
    discussions = Announcement.objects.all()
    leaves = LeaveRecords.objects.all()

    user_type = None
    user_role = None

    if hasattr(request.user, 'applicants'):
        user_type = 'applicant'
    elif hasattr(request.user, 'employees'):
        user_type = 'employee'
        user_role = request.user.employees.role
    
    dashboard_stats = {
        'total_applicants': applicants.count(),
        'total_job_openings': job_openings.count(),
        'total_employees': all_employees.count(),
        'total_discussions': discussions.count(),
        'total_leaves': leaves.count(),
    }
    
    username = request.user.username
    
    context = {
        'user_type': user_type,
        'user_role': user_role,
        'current_month_data_json': json.dumps(list(current_month_data), cls=DjangoJSONEncoder),
        'last_month_data_json': json.dumps(list(last_month_data), cls=DjangoJSONEncoder),
        'applicants': applicants,
        'job_openings': job_openings,
        'all_employees': all_employees,
        'discussions': discussions,
        'leaves': leaves,
        'dashboard_stats': dashboard_stats,
        'username': username
    }
    if hasattr(request.user, 'employees') and request.user.employees.role == 'hr_admin':
        # User is an HR admin and can view the page
        return render(request, 'index.html', context)
    else:
        # User is not an HR admin
        # Option 1: Redirect to another page
        # return redirect('some_other_view')

        # Option 2: Return a 'forbidden' HTTP response
        return redirect('login')

@login_required
def employee_dashboard(request):
    employee = Employees.objects.get(user=request.user)
    
    if employee.role != 'employee':
        return redirect('login')  # Redirect non-employees

    # Query for the number of announcements
    total_announcements = Announcement.objects.count()

    # Query for the number of leaves
    total_leaves = LeaveRecords.objects.filter(employee=employee).count()

    # Query for the number of job openings
    total_job_openings = JobOpenings.objects.count()

    # Query for the number of applicants
    total_applicants = Applicants.objects.count()

    # Display job openings
    job_openings_display = JobOpenings.objects.all()

    # Calculate leave days
    total_days_taken = calculate_leave_days(employee)
    remaining_days = 30 - total_days_taken

    context = {
        'dashboard_stats': {
            'total_announcements': total_announcements,
            'total_leaves': total_leaves,
            'total_job_openings': total_job_openings,
            'total_applicants': total_applicants,
            'job_openings': job_openings_display,
        },
        'leave_data': {
            'total_days_taken': total_days_taken,
            'remaining_days': remaining_days
        }
    }
    if hasattr(request.user, 'employees'):
        # User is an employee and can view the page
        return render(request, 'empDash.html', context)
    else:
        return HttpResponseForbidden("You are not authorized to view this page.")

@login_required
def applicant_dashboard(request):
    username = request.user.username
       # Ensure the user is logged in
    if not request.user.is_authenticated:
        # Redirect to login or handle unauthenticated user
        pass

     # Get the Applicants instance for the logged-in user
    applicant = Applicants.objects.get(user=request.user)
    # Query for the number of applied jobs for the logged-in applicant
    applied_jobs_count = ApplicantJob.objects.filter(applicant_id=applicant).count()

    # Query for the number of evaluations for the logged-in user

    evaluations_count = EvaluationReview.objects.filter(applicant_id=applicant).count()

    # Query for the number of announcements
    announcements_count = Announcement.objects.all().count()

    # Query for the number of job openings
    job_openings_count = JobOpenings.objects.all().count()

    # Query for the applicant's job applications
    applicant_jobs = ApplicantJob.objects.filter(applicant_id=applicant)

        # Get the status of each application
    application_statuses = applicant_jobs.values('status')  # Assuming JobOpenings model has a 'title' field

    job_openings_display = JobOpenings.objects.all()

    # Aggregate job applications by department
    department_application_counts = ApplicantJob.objects.values(
        'opening__department__department_name'
    ).annotate(count=Count('opening__department'))

    # Serialize for JavaScript
    department_application_counts_json = json.dumps(list(department_application_counts), cls=DjangoJSONEncoder)



    context = {
        'username': username,
        'dashboard_stats': {
            'job_openings': job_openings_display,
            'total_applied_jobs': applied_jobs_count,
            'total_evaluations': evaluations_count,
            'total_announcements': announcements_count,
            'total_job_openings': job_openings_count,
            'application_statuses': application_statuses,
            'department_application_counts_json': department_application_counts_json,
            'department_application_counts': department_application_counts,
        }
    }

    return render(request, 'AppDash.html', context)

@login_required
def employees_list(request):
    username = request.user.username
    employees = Employees.objects.all()
    return render(request, 'Employees.html', {'username': username, 'employees': employees})

@login_required
def ApplicationManagement(request):
    username = request.user.username
    return render(request, "ApplicationManagement.html", {'username': username})

@login_required
def Discussions(request):
    username = request.user.username
    return render(request, "Discussions.html", {'username': username})

@login_required
def employee_details(request, employee_id):
    username = request.user.username
    employee = get_object_or_404(Employees, pk=employee_id)
    
    # Pass the employee details and username to the template for rendering
    return render(request, 'employee_details.html', {'employee': employee, 'username': username})

@login_required
def opening_details(request, opening_id):
    opening = get_object_or_404(JobOpenings, pk=opening_id)
    context = {'opening': opening}
    return render(request, 'opening_details.html', context)

def opening_details_no_log(request, opening_id):
    opening = get_object_or_404(JobOpenings, pk=opening_id)
    context = {'opening': opening}
    return render(request, 'opening_details_no_log.html', context)

#@login_required
#def userProfile(request):
#    user_profile = Applicants.objects.filter(user=request.user).first()
#    return render(request, "userProfile.html", {'user_profile': user_profile})


# @login_required
# def edit_user_profile(request):
#     context = {}
#       # Adding username to the context
#     context['username'] = request.user.username
#     if hasattr(request.user, 'applicants'):
#         profile = get_object_or_404(Applicants, user=request.user)
#         form_class = ApplicantForm
#         template_name = 'edit_applicant_profile.html'

#         # Adding applicant's name to the context
#         context['profile_name'] = profile.name

#     elif hasattr(request.user, 'employees'):
#         profile = get_object_or_404(Employees, user=request.user)
#         form_class = EmployeeForm
#         template_name = 'edit_employee_profile.html'

#         # Adding employee's name and job title to the context
#         context['profile_name'] = profile.name
#         context['employee_job'] = profile.job.name  # Assuming 'job' is a ForeignKey and has a 'name' field
#         context['department_name'] = profile.department.department_name  # Assuming 'department' has a 'department_name' field
#         context['location_city'] = profile.location.city  # Assuming 'location' has a 'city' field
#     else:
#         # Handle case where the user is neither Applicant nor Employee
#         return redirect('some_default_view')

#     if request.method == 'POST':
#         form = form_class(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('userProfile')  # Redirect to a profile view or other
#     else:
#         form = form_class(instance=profile)

#     context['form'] = form
#     return render(request, template_name, context)

@login_required
def edit_user_profile(request):
    context = {}
    context['username'] = request.user.username

    if hasattr(request.user, 'applicants'):
        profile = get_object_or_404(Applicants, user=request.user)
        form_class = ApplicantForm
        template_name = 'edit_applicant_profile.html'
        context['profile_name'] = profile.name

    elif hasattr(request.user, 'employees'):
        profile = get_object_or_404(Employees, user=request.user)
        form_class = EmployeeForm
        template_name = 'edit_employee_profile.html'
        context['profile_name'] = profile.name
        context['employee_job'] = profile.job.name
        context['department_name'] = profile.department.department_name
        context['location_city'] = profile.location.city
        print("Job Name:", profile.job.name)
    else:
        return redirect('some_default_view')

    if request.method == 'POST':
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('userProfile')
    else:
        form = form_class(instance=profile)

    context['form'] = form
    return render(request, template_name, context)

@login_required
def Vaccincies(request):
    username = request.user.username

    user_role = get_user_role(request.user)
    
    context = {
        'username': username,
        'user_role': user_role
        }
        # ... your existing context variables ...

    return render(request, "Vaccincies.html", context)


def Vaccincies2(request):
    all_openings = JobOpenings.objects.order_by('-date_posted')
    context = {
        'all_openings': all_openings,
    }
    return render(request, "vaccan_no_log.html", context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import PerformanceReview, EvaluationReview, Employees  # Adjust with your actual model names

@login_required
def Report(request):
    username = request.user.username
    
    # Initialize querysets
    employee_reviews = PerformanceReview.objects.none()
    applicant_reviews = EvaluationReview.objects.none()
    
    # Determine if the user is an HR admin
    try:
        employee = Employees.objects.get(user=request.user)
        is_hr_admin = employee.role == 'hr_admin'
    except Employees.DoesNotExist:
        employee = None
        is_hr_admin = False

    # Fetch all records for HR admin, specific records for others
    if is_hr_admin:
        employee_reviews = PerformanceReview.objects.all()
        applicant_reviews = EvaluationReview.objects.all()
    else:
        employee_reviews = PerformanceReview.objects.filter(employee=employee)
        try:
            applicant = Applicants.objects.get(user=request.user)
            applicant_reviews = EvaluationReview.objects.filter(applicant_id=applicant)
        except Applicants.DoesNotExist:
            applicant_reviews = EvaluationReview.objects.none()

    context = {
        'employee_reviews': employee_reviews,
        'applicant_reviews': applicant_reviews,
        'username': username,
        'is_hr_admin': is_hr_admin
    }

    return render(request, 'Report.html', context)





@login_required
def PerformanceReview_detail(request, review_id):
    username = request.user.username
    review = get_object_or_404(PerformanceReview, pk=review_id)  
    context = {'review': review,
               'username': username
               }
    return render(request, 'performance_detail.html', context)

@login_required
def evaluationreview_detail(request, review_id):
    username = request.user.username
    review = get_object_or_404(EvaluationReview, pk=review_id)
    context = {'review': review,
               'username': username
               }
    return render(request, 'evaluationreview_detail.html', context)

@login_required
def EvaluateEmployee(request):
    username = request.user.username
    return render(request, "EvaluateEmployee.html", {'username': username})

@login_required
def EvaluateApplicant(request, applicant_id):
    username = request.user.username
    applicant = get_object_or_404(Applicants, pk=applicant_id)

    if request.method == 'POST':
        form = EvaluationReviewForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.applicant_id_id = applicant.pk  # Assign the primary key of the applicant
            evaluation.save()
            return redirect('ApplicationManagement')
    else:
        form = EvaluationReviewForm()
    
    context = {
        'form': form,
        'applicant': applicant,
        'username':username
    }
    return render(request, 'EvaluateApplicant.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employees, PerformanceReview
from .forms import PerformanceReviewForm

@login_required
def evaluate_employee(request, employee_id): 
    username = request.user.username

    employee = get_object_or_404(Employees, pk=employee_id)
    #reviewer = employee.user  # Assuming request.user.employee is the related Employee instance of the logged-in user
    
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.employee = employee
            #review.reviewer = reviewer
            review.save()
            return redirect('Employees')  # Replace with your redirect URL
    else:
        form = PerformanceReviewForm()
    
    context = {
        'form': form,
        'employee': employee,
        'username':username
    }
    return render(request, 'EvaluateEmployee.html', context)




#@login_required(login_url='/accounts/login/?next=/apply/')
@login_required
def apply(request, opening_id=None):
    username = request.user.username

    if opening_id:
        opening = JobOpenings.objects.get(pk=opening_id)

        if request.method == 'POST':
            form = ApplicantJobForm(request.POST, request.FILES)
            if form.is_valid():
                applicant_job = form.save(commit=False)
                applicant_job.applicant = request.user.applicants
                applicant_job.opening = opening
                applicant_job.status = 'Pending'
                applicant_job.application_date = timezone.now()

                if 'cv' in request.FILES:
                    handle_uploaded_file2(request.FILES['cv'])
                    applicant_job.cv ="\cvs\{0}".format(request.FILES['cv'].name)

                applicant_job.save()
                return redirect('ApplicationManagement')
        else:
            form = ApplicantJobForm()
        
        context = {'form': form, 'opening': opening, 'username': username}
        return render(request, 'apply.html', context)
    else:
        return render(request, "apply.html", {'username': username})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import User, Applicants

from .forms import SignUpForm, UserSignUpForm, EvaluationReviewForm

def signup(request):
    if request.method == 'POST':
        applicants_form = SignUpForm(request.POST)
        user_form = UserSignUpForm(request.POST)
        
        if applicants_form.is_valid() and user_form.is_valid():
            user = user_form.save()  # Save User data
            
            applicants = applicants_form.save(commit=False)  # Save Applicants data
            applicants.user = user  # Link the created user to the applicants
            applicants.save()
            
            # Log in the user
            login(request, user)
            
            return redirect(reverse('applicant_dashboard'))  # Redirect after successful sign-up
    else:
        applicants_form = SignUpForm()
        user_form = UserSignUpForm()
    
    return render(request, 'signup.html', {'applicants_form': applicants_form, 'user_form': user_form})

#view to get all applicant data
#def applicant_list(request, applicant_id=None):
 #   if applicant_id:
  #      applicant = Applicants.objects.get(pk=applicant_id)
   #     return render(request, 'ApplicationManagement.html', {'applicant': applicant})
    #else:
     #   applicants = Applicants.objects.all()
      #  username = request.user.username
       # context = {'applicants': applicants, 'username': username}
        #return render(request, 'ApplicationManagement.html', context)
    
from django.db.models import Prefetch

@login_required
def applicant_list(request):
    # Fetch all applicants along with their related ApplicantJob details, ordered by application date
    applicants_with_jobs = Applicants.objects.prefetch_related(
        'applied_jobs'  # Assuming 'applied_jobs' is the related name for the ApplicantJob ForeignKey in the Applicants model
    ).order_by('-applied_jobs__application_date')
    
    username = request.user.username
    context = {'applicants': applicants_with_jobs, 'username': username}
    return render(request, 'ApplicationManagement.html', context)


@login_required
def approve_applicant_job(request, applicantjob_id):
    # Get the ApplicantJob object, or return a 404 if not found
    applicant_job = get_object_or_404(ApplicantJob, pk=applicantjob_id)

    # Update the status to 'approved'
    applicant_job.status = 'Approved'
    applicant_job.save()

    # Redirect back to the applicant list or wherever is appropriate
    return redirect('applicant_list')

def all_job_openings(request):
    all_openings = JobOpenings.objects.order_by('-date_posted')
    username = request.user.username
    context = {'all_openings': all_openings, 'username': username}
    return render(request, 'Vaccincies.html', context)

#view to get all employee data
@login_required
def employee_details_dash(request, id):
    employee = employee.objects.get(id=id)
    return render(request, 'index.html', {'employee':employee})
    
   # return HttpResponse(request, 'HomePage')
@login_required
def logout_view(request):
    logout(request)
    # Redirect to a page after logout 
    return redirect('login')

@login_required
def addVacancy(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('/Vaccincies')
    else:
        form = VacancyForm()
    
    username = request.user.username
    return render(request, 'addVacancy.html', {'form': form, 'username': username})

@login_required
def delete_vacancy(request, opening_id):
    # Fetch the instance to be deleted
    opening = get_object_or_404(JobOpenings, opening_id=opening_id)
    
    # Delete the instance
    opening.delete()
    
    return redirect('/Vaccincies')

@login_required
def delete_applicant(request, applicant_id):
    # Fetch the applicant instance to be deleted
    applicant = get_object_or_404(Applicants, applicant_id=applicant_id)
    
    # Delete the applicant instance
    applicant.delete()
    
    return redirect('/ApplicationManagement')

@login_required
def announcement_list(request):
    username = request.user.username
    announcements = Announcement.objects.order_by('-date_created').all()
    return render(request, 'Discussions.html', {'announcements': announcements, 'username': username})

@login_required
def create_announcement(request):
    username = request.user.username
    if request.method == "POST":
        myForm = AnnouncementForm(request.POST, request.FILES)
        if myForm.is_valid():
            handle_uploaded_file(request.FILES['image_path'])

            title=myForm.cleaned_data["title"]
            content=myForm.cleaned_data["content"]
            image_path="\img\\announcement_images\{0}".format(request.FILES['image_path'].name)

            announcement_obj=Announcement(title=title,content=content,image_path=image_path)
            announcement_obj = Announcement(
            title=title,
            content=content,
            image_path=image_path,
            creator=request.user  # Assign the current user as the creator
        )
            announcement_obj.save()
            return redirect('Discussions')

    else:
        myForm = AnnouncementForm()
    return render(request, "create_announcement.html", {"myForm": myForm, 'username': username})


@login_required
def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)

    # Check if the user is the creator or an HR admin
    if request.user == announcement.creator or request.user.groups.filter(name='HR Admin').exists():
        announcement.delete()
        messages.success(request, "Announcement deleted successfully.")
        return redirect('Discussions')
    else:
        messages.error(request, "You don't have permission to delete this announcement.")
        return redirect('Discussions')


import xlwt

@login_required
def download_employee_list(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="employee_list.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Employees')

    # Column headers
    row_num = 0
    columns = ['Employee ID', 'Name', 'Mobile Number', 'Email', 'Job']
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Writing data
    employees = Employees.objects.all()
    for employee in employees:
        row_num += 1
        ws.write(row_num, 0, employee.employee_id)
        ws.write(row_num, 1, employee.name)
        ws.write(row_num, 2, str(employee.mobile_number))
        ws.write(row_num, 3, employee.email)
        ws.write(row_num, 4, employee.job.name)

    wb.save(response)
    return response

@login_required
def download_applicant_list(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="applicant_list.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Applicants')

    # Column headers
    row_num = 0
    columns = ['Applicant ID', 'Name', 'Mobile Number', 'Email', 'Applied To', 'Status']
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Writing data
    applicants = Applicants.objects.all()
    for applicant in applicants:
        for applicant_job in applicant.applied_jobs.all():
            row_num += 1
            ws.write(row_num, 0, applicant.applicant_id)
            ws.write(row_num, 1, applicant.name)
            ws.write(row_num, 2, str(applicant.mobile_number))
            ws.write(row_num, 3, applicant.email)
            ws.write(row_num, 4, applicant_job.opening.job_name)
            ws.write(row_num, 5, applicant_job.status)

    wb.save(response)
    return response



from django.conf import settings

@login_required
def applicant_details(request, applicant_id):
    username = request.user.username
    applicant = get_object_or_404(Applicants, pk=applicant_id)
    applied_jobs = applicant.applied_jobs.all()
    evaluations = EvaluationReview.objects.filter(applicant_id=applicant_id)

    # Get URLs of uploaded CVs
    cv_urls = [settings.STATIC_URL + 'cvs/' + os.path.basename(job.cv.name) for job in applied_jobs if job.cv]


    context = {
        'username': username,
        'applicant': applicant,
        'applied_jobs': applied_jobs,
        'evaluations': evaluations,
        'cv_urls': cv_urls,  # Add the CV URLs to the context
    }
    return render(request, 'applicant_details.html', context)

  


from django.core.exceptions import ObjectDoesNotExist

@login_required
def apply_for_leave(request):
    username = request.user.username
    is_hr_admin = request.user.groups.filter(name='HR Admin').exists()
    print("Is HR Admin:", is_hr_admin)  # Add this line for debugging
    try:
        employee = Employees.objects.get(user=request.user)
    except Employees.DoesNotExist:
        return HttpResponse('Only Employees Can access this page')

    leave_choices = Leaves.objects.all()

    if request.method == 'POST':
        form = EmployeeLeaveForm(request.POST)
        if form.is_valid():
            leave_record = LeaveRecords()
            leave_record.employee = employee
            leave_record.leave = form.cleaned_data['leave']
            leave_record.from_date = form.cleaned_data['start_date']
            leave_record.to_date = form.cleaned_data['end_date']
            leave_record.status = 'Pending'
            leave_record.save()
            return redirect('Leaves')
    else:
        form = EmployeeLeaveForm()

    context = {
        'form': form,
        'username': username,
        'leave_choices': leave_choices
    }

    return render(request, 'apply_for_leave.html', context)

@login_required
def leaves_view(request):
    username = request.user.username
    show_all = request.GET.get('show_all', 'false').lower() == 'true'

    try:
        employee = Employees.objects.get(user=request.user)
        is_hr_admin = employee.role == 'hr_admin'
    except Employees.DoesNotExist:
        is_hr_admin = False

    if is_hr_admin and show_all:
        applied_leaves = LeaveRecords.objects.all()
    else:
        applied_leaves = LeaveRecords.objects.filter(employee=employee)

    context = {
        'applied_leaves': applied_leaves,
        'username': username,
        'is_hr_admin': is_hr_admin,
        'show_all': show_all  # Pass this to the template
    }

    return render(request, 'Leaves.html', context)
