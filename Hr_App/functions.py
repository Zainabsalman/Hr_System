from .models import Applicants, Employees


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