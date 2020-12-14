from django.urls import path

from .views import SignUpView, home, login, logout, create_fee, student_detail, list_student

app_name = 'crud'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('home/', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('student/detail/', student_detail, name='student_detail'),
    path('student/list/', list_student, name='list_student'),
    path('create/fee/', create_fee, name='create_fee'),
    # path('update/<int:pk>', UpdateStudent.as_view(), name='update'),
]
