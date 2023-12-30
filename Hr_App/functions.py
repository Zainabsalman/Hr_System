from .models import Applicants, Employees,LeaveRecords
from datetime import date
from django.db.models import Sum, F, ExpressionWrapper, fields

def handle_uploaded_file(file):
    with open('static/img/announcement_images/'+file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def handle_uploaded_file2(file):
    with open('static/cvs/'+file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def get_user_role(user):
    if not user.is_authenticated:
        return 'guest'
    
    if Employees.objects.filter(user=user).exists():
        return Employees.objects.get(user=user).role
    elif Applicants.objects.filter(user=user).exists():
        return 'applicant'
    
    return 'guest'


def calculate_leave_days(employee):
    current_year = date.today().year
    leaves = LeaveRecords.objects.filter(
        employee=employee, 
        from_date__year=current_year
    )

    total_days = 0
    for leave in leaves:
        # Calculate duration in days for each leave
        duration = (leave.to_date - leave.from_date).days + 1  # +1 if the end date is inclusive
        total_days += duration

    return total_days