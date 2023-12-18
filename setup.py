import datetime
import os 
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hr_System.settings')

django.setup()

from django.contrib.auth.hashers import make_password
from Hr_App.models import Employees, EmployeeQualification, EmployeeBenefits, EmployeePerformanceReview, EmployeeProfile, EvaluationReview, Applicants, ApplicantJob, Benefits, Qualifications, LeaveRecords, Leaves, Locations, JobOpenings, Jobs, Chat, ChatMessage, Department, ReportDepartment, Reports, PerformanceReview, SalaryGrades


try:

    job1 = Jobs(name= "Admin", 
                description=" overseeing and managing various administrative tasks within an organization")
    job2 = Jobs(name= "Tutor", 
                description=" provides academic support and guidance to students")
    job3 = Jobs(name= "Hr Manger", 
                description="oversees all aspects of the human resources function within an organization")
    job4 = Jobs(name= "IT Manager",
                description=" oversees the technology infrastructure and operations within an organization")

    job1.save()
    job2.save()
    job3.save()
    job4.save()

    location1 = Locations (
        country = "Bahrain",
        address = "122",
        city = "Manama",
        governorate =  "Capital governorate",
    )

    location2 = Locations (
        country = "Bahrain",
        address = "333",
        city = "Isa Town",
        governorate =  "Southern governorate",
    )

    location1.save()
    location2.save()

    Department1 = Department(
        department_name = "HR",
        description = "Human Resources",
    )

    Department2 = Department(
        department_name = "IT",
        description = "Information Technology",
    )

    Department3 = Department(
        department_name = "AD",
        description = "Administration",
    )

    Department4 = Department(
        department_name = "AS",
        description = "Academic Staff",
    )

    Department1.save()
    Department2.save()
    Department3.save()
    Department4.save()



    # Create Employees
    employee1 = Employees(name="zainab", dob="1990-01-01", email="employee1@example.com",
                        join_date="2023-01-01", mobile_number="1234567890",
                        job=job1, location=location1, department= Department1)
    employee1.save()

    employee2 = Employees(name="amira", dob="1995-02-02", email="employee2@example.com",
                        join_date="2023-02-02", mobile_number="9876543210",
                        job=job2, location=location2, department=Department2)
    employee2.save()

    # Create EmployeeProfile instances
    employee_profile1 = EmployeeProfile(employee=employee1, department="Department 1", 
                                        job_title="Job Title 1", profile_picture="profile_pictures/employee1.jpg")
    employee_profile1.save()

    employee_profile2 = EmployeeProfile(employee=employee2, department="Department 2", 
                                        job_title="Job Title 2", profile_picture="profile_pictures/employee2.jpg")
    employee_profile2.save()

    # Create DiscussionChat instances
    chat_message1 = ChatMessage(employee=employee1, content="Hello, Employee 2!")
    chat_message1.save()

    chat_message2 = ChatMessage(employee=employee2, content="Hi, Employee 1!")
    chat_message2.save()

    # Create Discussion instance
    chat = Chat(name="Employee Chat")
    chat.save()
    chat.participants.add(employee1, employee2)
    chat.messages.add(chat_message1, chat_message2)

    # Create PerformanceReview instance
    performance_review = PerformanceReview(score=8.5, review_date=datetime.datetime.now(), comments="Good performance")
    performance_review.save()

    # Create EmployeePerformanceReview instance
    employee_performance_review = EmployeePerformanceReview(review=performance_review, employee=employee1)
    employee_performance_review.save()

    # Create Applicants
    applicant1 = Applicants(name="Mohammed", dob="1992-03-03", email="applicant1@example.com",
                            mobile_number="5555555555")
    applicant1.save()

    applicant2 = Applicants(name="Oskar", dob="1994-04-04", email="applicant2@example.com",
                            mobile_number="6666666666")
    applicant2.save()


    # Create Qualifications instance
    qualification1 = Qualifications(degree="Bachelor's", institute="University 1", 
                                    graduation_year="2020", specialization="Specialization 1")
    qualification1.save()

    qualification2 = Qualifications(degree="Master's", institute="University 2",
                                    graduation_year="2022", specialization="Specialization 2")
    qualification2.save()

    # Create Benefits instance
    benefit1 = Benefits(name="Health Insurance", description="Health coverage")
    benefit1.save()

    benefit2 = Benefits(name="Retirement Plan", description="Retirement savings plan")
    benefit2.save()

    # Create SalaryGrades instance
    salary_grade1 = SalaryGrades(job=job1, salary_range=70000)
    salary_grade1.save()

    salary_grade2 = SalaryGrades(job=job2, salary_range=80000)
    salary_grade2.save()

    # Create Reports instance
    report = Reports(report_name="Monthly Report", report_type="Monthly", date=datetime.datetime.now(),
                    description="Monthly summary")
    report.save()

    # Create Leaves instance
    leave1 = Leaves(type="Annual Leave", description="Paid time off")
    leave1.save()

    leave2 = Leaves(type="Sick Leave", description="Paid time off")
    leave2.save()

    # Create EvaluationReview instance
    evaluation_review = EvaluationReview(score=8.0, review_date=datetime.datetime.now(), 
                                        applicant_id=applicant1, comments="Evaluated")
    evaluation_review.save()

    # Create ReportDepartment instance
    report_department = ReportDepartment(department=Department1, report=report)
    report_department.save()

    # Create vaccnicies instance
    job_opening = JobOpenings(job=job1, department=Department1, date_posted=datetime.datetime.now(), 
                            deadline=datetime.datetime.now())
    job_opening.save()

    # Create ApplicantJob instance
    applicant_job = ApplicantJob(applicant=applicant1, opening=job_opening, 
                                application_date=datetime.datetime.now(), status="Applied")
    applicant_job.save()

    # Create EmployeeQualification instance
    employee_qualification = EmployeeQualification(qualification=qualification1, employee=employee1)
    employee_qualification.save()

    # Create LeaveRecords instance
    leave_record = LeaveRecords(employee=employee1, leave=leave1, from_date=datetime.datetime.now(), 
                                to_date=datetime.datetime.now(), status="Approved")
    leave_record.save()

    # Create EmployeeBenefits instance
    employee_benefit = EmployeeBenefits(employee=employee1, benefit=benefit1)
    employee_benefit.save()
    
except Exception as e:
    print(f"An error occurred: {e}")