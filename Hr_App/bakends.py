from django.contrib.auth.backends import ModelBackend
from .models import Applicants, Employees
from django.contrib.auth import authenticate
class UserTypeBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        # Check user type and authenticate accordingly
        user = None

        # Authenticate the user based on their type
        if Applicants.objects.filter(email=username).exists():
            applicant = Applicants.objects.get(email=username)
            user = authenticate(request, username=applicant.email, password=password)
        elif Employees.objects.filter(email=username).exists():
            employee = Employees.objects.get(email=username)
            user = authenticate(request, username=employee.email, password=password)
        
        return user