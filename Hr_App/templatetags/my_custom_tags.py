from django import template
from ..models import Employees, Applicants

register = template.Library()

@register.simple_tag
def get_user_role(user):
    if not user.is_authenticated:
        return 'guest'
    
    if Employees.objects.filter(user=user).exists():
        return Employees.objects.get(user=user).role
    elif Applicants.objects.filter(user=user).exists():
        return 'applicant'
    
    return 'guest'
