import datetime
import os 
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hr_System.settings')

django.setup()

from django.contrib.auth.hashers import make_password
from Hr_App.models import Employees, EmployeeQualification, EmployeeBenefits, EmployeePerformanceReview, EmployeeProfile, EvaluationReview, Applicants, ApplicantJob, Benefits, Qualifications, LeaveRecords, Leaves, Locations, JobOpenings, Jobs, Chat, ChatMessage, Department, ReportDepartment, Reports, PerformanceReview, SalaryGrades

# # Create Leaves instance
# leave1 = Leaves(type="Annual Leave", description="Paid time off")
# leave1.save()

# leave2 = Leaves(type="Sick Leave", description="Paid time off")
# leave2.save()

# # Creating job instances
# job1 = Jobs(name="Assistant Tutor", 
#             description="Responsible for assisting lead tutors in preparing lesson plans, managing classrooms, and supporting student learning activities.")

# job2 = Jobs(name="Tutor", 
#             description="Provides academic support and guidance to students, helping them understand complex subjects and improve their academic performance.")

# job3 = Jobs(name="HR Manager", 
#             description="Oversees all aspects of the human resources function within the school, including recruitment, staff development, and employee relations.")

# job4 = Jobs(name="IT Manager",
#             description="Manages the school's technology infrastructure, ensuring the effective operation of computer systems, networks, and educational technology tools.")

# job5 = Jobs(name="Principal",
#             description="Leads the school, responsible for setting educational standards, managing staff, and ensuring a safe and effective learning environment.")

# job6 = Jobs(name="School Counselor",
#             description="Provides counseling services to students, addressing their academic, personal, and social development needs.")

# job7 = Jobs(name="Librarian",
#             description="Manages the school library, helping students and staff access educational resources and promoting literacy and reading.")

# job8 = Jobs(name="Physical Education Teacher",
#             description="Teaches physical education classes, promoting physical fitness and coordinating sports activities.")

# job9 = Jobs(name="School Nurse",
#             description="Provides healthcare services to students and staff, managing medical emergencies and promoting health education.")

# job10 = Jobs(name="Administrative Assistant",
#              description="Assists in the daily administrative operations of the school, handling communications, schedules, and clerical tasks.")

# # Saving the job instances
# job1.save()
# job2.save()
# job3.save()
# job4.save()
# job5.save()
# job6.save()
# job7.save()
# job8.save()
# job9.save()
# job10.save()

# job5 = Jobs(name="School Secretary",
#             description="Manages the administrative activities of the school, including handling correspondence, scheduling appointments, and maintaining records.")
# job6 = Jobs(name="Cafeteria Manager",
#             description="Oversees the operation of the school cafeteria, including meal planning, food preparation, and staff management.")
# job7 = Jobs(name="Maintenance Supervisor",
#             description="Responsible for the maintenance and repair of school facilities, ensuring a safe and functional environment for students and staff.")
# job8 = Jobs(name="School Psychologist",
#             description="Provides psychological services and counseling to students, supporting their emotional and educational development.")
# job9 = Jobs(name="Art Teacher",
#             description="Teaches art classes, encouraging creativity and artistic expression among students.")
# job10 = Jobs(name="Music Teacher",
#              description="Instructs students in music theory and practice, fostering musical talent and appreciation.")
# job11 = Jobs(name="Science Teacher",
#              description="Teaches science subjects, facilitating students' understanding of scientific concepts and principles.")
# job12 = Jobs(name="Mathematics Teacher",
#              description="Educates students in mathematics, helping them develop critical thinking and problem-solving skills.")
# job13 = Jobs(name="History Teacher",
#              description="Teaches history, encouraging students to explore and understand historical events and contexts.")
# job14 = Jobs(name="Language Teacher",
#              description="Instructs students in foreign languages, promoting language skills and cultural awareness.")


# job5.save()
# job6.save()
# job7.save()
# job8.save()
# job9.save()
# job10.save()
# job11.save()
# job12.save()
# job13.save()
# job14.save()


# # Existing job instances
# job1 = Jobs(name="Assistant Tutor", 
#             description="Responsible for overseeing and managing various administrative tasks within an organization.")
# job2 = Jobs(name="Tutor", 
#             description="Provides academic support and guidance to students.")
# job3 = Jobs(name="HR Manager", 
#             description="Oversees all aspects of the human resources function within an organization.")
# job4 = Jobs(name="IT Manager",
#             description="Oversees the technology infrastructure and operations within an organization.")

# Additional job instances for a university
job5 = Jobs(name="Research Assistant",
            description="Assists in academic research, data collection, and analysis, often in a specific field of study.")
job6 = Jobs(name="Admissions Officer",
            description="Manages the student admissions process, from application review to conducting interviews and making admission decisions.")
job7 = Jobs(name="Campus Security Officer",
            description="Ensures the safety and security of the university campus, students, and staff.")
job8 = Jobs(name="Resident Advisor",
            description="Provides guidance and support to students living in university housing, promoting a positive living environment.")
job9 = Jobs(name="Academic Advisor",
            description="Guides students in course selection, career advice, and academic planning to achieve their educational goals.")
job10 = Jobs(name="Laboratory Technician",
             description="Supports academic and research labs, managing equipment and assisting in experiments.")
job11 = Jobs(name="Library Assistant",
             description="Assists in the operation of the university library, including helping students find resources and maintaining collections.")
job12 = Jobs(name="Sports Coach",
             description="Coaches university sports teams, developing athletic programs and mentoring student-athletes.")
job13 = Jobs(name="Student Services Coordinator",
             description="Coordinates various student services and activities, enhancing the overall student experience.")
job14 = Jobs(name="Alumni Relations Officer",
             description="Manages relationships with university alumni, organizing events and facilitating alumni engagement.")

# Saving the job instances
# job1.save()
# job2.save()
# job3.save()
# job4.save()
job5.save()
job6.save()
job7.save()
job8.save()
job9.save()
job10.save()
job11.save()
job12.save()
job13.save()
job14.save()


# # Creating department instances
# Department1 = Department(
#     department_name="Human Resources",
#     description="Manages all human resources functions, including staff recruitment, training, and employee welfare."
# )

# Department2 = Department(
#     department_name="IT",
#     description="Responsible for maintaining the school's information technology infrastructure, including hardware, software, and network resources."
# )

# Department3 = Department(
#     department_name="Admin",
#     description="Handles the school's administrative tasks, including finance, legal, and general operations."
# )

# Department4 = Department(
#     department_name="Academic Staff",
#     description="Comprises the teaching staff responsible for delivering educational content and assessing student performance."
# )

# Department5 = Department(
#     department_name="Student Affairs",
#     description="Focuses on student services including admissions, extracurricular activities, and student support."
# )

# Department6 = Department(
#     department_name="Facilities Management",
#     description="Manages the maintenance and operations of school facilities and grounds."
# )

# Department7 = Department(
#     department_name="Library Services",
#     description="Oversees the school library, providing access to learning resources and research support."
# )

# Department8 = Department(
#     department_name="Health Services",
#     description="Provides health care and medical services to students and staff."
# )

# Department9 = Department(
#     department_name="Counseling and Guidance",
#     description="Offers counseling services to support the emotional and psychological well-being of students."
# )

# Department10 = Department(
#     department_name="Extracurricular Activities",
#     description="Manages and coordinates various extracurricular and recreational programs for students."
# )

# # Saving the department instances
# Department1.save()
# Department2.save()
# Department3.save()
# Department4.save()
# Department5.save()
# Department6.save()
# Department7.save()
# Department8.save()
# Department9.save()
# Department10.save()


# # Creating location instances
# location1 = Locations(
#     country = "Bahrain",
#     address = "122",
#     city = "Manama",
#     governorate = "Capital Governorate",
# )

# location2 = Locations(
#     country = "Bahrain",
#     address = "333",
#     city = "Isa Town",
#     governorate = "Southern Governorate",
# )

# location3 = Locations(
#     country = "Bahrain",
#     address = "444",
#     city = "Riffa",
#     governorate = "Southern Governorate",
# )

# location4 = Locations(
#     country = "Bahrain",
#     address = "555",
#     city = "Muharraq",
#     governorate = "Muharraq Governorate",
# )

# location5 = Locations(
#     country = "Bahrain",
#     address = "666",
#     city = "Hamad Town",
#     governorate = "Northern Governorate",
# )

# location6 = Locations(
#     country = "Bahrain",
#     address = "777",
#     city = "A'ali",
#     governorate = "Central Governorate",
# )

# location7 = Locations(
#     country = "Bahrain",
#     address = "888",
#     city = "Sitra",
#     governorate = "Central Governorate",
# )

# location8 = Locations(
#     country = "Bahrain",
#     address = "999",
#     city = "Juffair",
#     governorate = "Capital Governorate",
# )

# location9 = Locations(
#     country = "Bahrain",
#     address = "1010",
#     city = "Budaiya",
#     governorate = "Northern Governorate",
# )

# location10 = Locations(
#     country = "Bahrain",
#     address = "1111",
#     city = "Zallaq",
#     governorate = "Southern Governorate",
# )

# location11 = Locations(
#     country = "Bahrain",
#     address = "1212",
#     city = "Adliya",
#     governorate = "Capital Governorate",
# )

# location12 = Locations(
#     country = "Bahrain",
#     address = "1313",
#     city = "Jidhafs",
#     governorate = "Northern Governorate",
# )

# # Saving the location instances
# location1.save()
# location2.save()
# location3.save()
# location4.save()
# location5.save()
# location6.save()
# location7.save()
# location8.save()
# location9.save()
# location10.save()
# location11.save()
# location12.save()
