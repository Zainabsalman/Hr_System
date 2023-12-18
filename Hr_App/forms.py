from django import forms

from .functions import handle_uploaded_file
from .models import Announcement, EmployeeLeave, Employees, JobOpenings, ApplicantJob, Applicants, EvaluationReview, PerformanceReview
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


    
class SignUpForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    mobile_number = forms.CharField(max_length=8, min_length=8)
    class Meta:
        model = Applicants
        fields = ['name', 'mobile_number', 'dob', 'email']

class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2']

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicants
        fields = ['name', 'mobile_number', 'dob', 'email']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = ['name', 'dob', 'email', 'mobile_number', 'job', 'location', 'department', 'role']

class EvaluationReviewForm(forms.ModelForm):
    applicant_id = forms.IntegerField(disabled=True, required=False, label='Applicant ID')

    class Meta:
        model = EvaluationReview
        fields = [
           'score',
            'review_date',
            'comments',
            'communication_skills',
            'facial_disclosure',
            'eye_contact',
            'posture',
            'self_control',
            'personality',
            'handling_question_1',
            'handling_question_2',
            'applicant_id',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance:
                self.fields['applicant_id'].initial = instance.pk                


    #def __init__(self, *args, **kwargs):
     #   instance = kwargs.get('instance')
      #  super().__init__(*args, **kwargs)
       # if instance:
        #    self.fields['applicant_id'].queryset = Applicants.objects.filter(pk=instance.pk)

         #   self.fields['applicant_id'].initial = applicant.pk
          #  self.fields['applicant_name'].initial = applicant.name
           # self.fields['applicant_email'].initial = applicant.email
            #self.fields['applicant_dob'].initial = applicant.dob
            #self.fields['applicant_mobile_number'].initial = applicant.mobile_number


class VacancyForm(forms.ModelForm):
    class Meta:
        model = JobOpenings
        fields = ['job', 'department', 'date_posted', 'deadline', 'description']
        
    def clean(self):
        cleaned_data = super().clean()
        date_posted = cleaned_data.get('date_posted')
        deadline = cleaned_data.get('deadline')

        # Check if date_posted and deadline are provided
        if date_posted and deadline:
            # Check if the deadline is before the date posted
            if deadline < date_posted:
                raise ValidationError(_("Deadline must be after the Date Posted"))

        # Check if the date_posted is in the future
        today = datetime.date.today()
        if date_posted and date_posted > today:
            raise ValidationError(_("Date Posted cannot be in the future"))

        return cleaned_data
  


class ApplicantJobForm(forms.ModelForm):
    class Meta:
        model = ApplicantJob
        fields = ['reason_for_hire', 'application_date']  # Include only 'reason_for_hire' and 'application_date'

    def __init__(self, *args, **kwargs):
        super(ApplicantJobForm, self).__init__(*args, **kwargs)
        for field_name in self.Meta.fields:
            if field_name != 'status':  # Exclude the 'status' field from being displayed
                self.fields[field_name].widget = forms.HiddenInput()


class PerformanceReviewForm(forms.ModelForm):
    employee_id = forms.IntegerField(disabled=True, required=False, label='Employee ID')
    class Meta:
        model = PerformanceReview
        fields = [
            'employee', 'reviewer', 'score', 'review_date', 'comments',
            'communication_skills', 'teamwork', 'problem_solving',
            'adaptability', 'punctuality'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance:
                self.fields['employee_id'].initial = instance.pk    
        # Add any customization for fields here if needed
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'image_path']  # Ensure 'image_path' is part of your model fields

    # Override the field to use FileField for uploading files
    image_path = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))  # Adjust widget as needed

class EmployeeLeaveForm(forms.ModelForm):
    class Meta:
        model = EmployeeLeave
        fields = ['leave', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }