"""Hr_System URL Configuration"""

from django.conf import settings
from django.contrib import admin
from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

"#importing views.py"
#from django.conf.urls import url 
from Hr_App import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.custom_login, name='logIn'),
    path('admin/', admin.site.urls),
    path('Discussions/', views.announcement_list, name='Discussions'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('userProfile/', views.edit_user_profile, name='userProfile'),
    path('Employees/', views.employees_list, name='Employees'),
    path('Leaves/', views.leaves_view, name='Leaves'),
    path('Vaccincies/', views.all_job_openings, name='all_job_openings'),
    path('Vaccincies/', views.Vaccincies, name='Vaccincies'),
    path('Report/', views.Report, name='Report'),
    path('apply/', views.apply, name='apply'),
    path('apply/<int:opening_id>/', views.apply, name='apply_to_job'),
    path('ApplicationManagement/', views.applicant_list, name='applicant_list'),
    path('ApplicationManagement/', views.ApplicationManagement, name='ApplicationManagement'),
    path('addVacancy/', views.addVacancy, name='addVacancy'),
    path('delete_vacancy/<str:opening_id>/', views.delete_vacancy, name='delete_vacancy'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='logIn.html',
        success_url='/',  # Set the success URL to '/' (index page)
    ), name='login'),
    path('vaccan_no_log/', views.Vaccincies2, name='Vaccincies2'),
    path('logout/', views.logout_view, name='logout'),
    path('EvaluateApplicant/<int:applicant_id>/', views.EvaluateApplicant, name='EvaluateApplicant'),
    path('deleteApplicantJob/<int:applicantjob_id>/', views.delete_applicant_job, name='delete_applicant_job'),
    path('evaluate_employee/<int:employee_id>/', views.evaluate_employee, name='evaluate_employee'),
    path('employee_details/<int:employee_id>/', views.employee_details, name='employee_details'),
    path('applicant_details/<int:applicant_id>/', views.applicant_details, name='applicant_details'),
    path('download-employees/', views.download_employee_list, name='download_employees'),
    path('download-applicants/', views.download_applicant_list, name='download_applicants'),
    path('download-applicants/', views.download_applicant_list, name='download_applicants'),
    path('dashboard/employee/', views.employee_dashboard, name='employee_dashboard'),
    path('dashboard/applicant/', views.applicant_dashboard, name='applicant_dashboard'),
    path('evaluationreviews/<int:review_id>/', views.evaluationreview_detail, name='evaluationreview_detail'),
    path('evaluations/<int:review_id>/', views.PerformanceReview_detail, name='PerformanceReview_detail'),
    path('openings/<int:opening_id>/', views.opening_details, name='opening_details'),
    path('openings_no_log/<int:opening_id>/', views.opening_details_no_log, name='opening_details_no_log'),
    path('userProfile/edit/', views.edit_user_profile, name='edit_applicant_profile'),
    path('apply_for_leave/', views.apply_for_leave, name='apply_for_leave'),
    path('announcement/delete/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
    path('approve_applicant_job/<int:applicantjob_id>/', views.approve_applicant_job, name='approve_applicant_job'),

]

