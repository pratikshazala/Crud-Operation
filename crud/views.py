from datetime import datetime
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, UpdateView, ListView
from knpay_plugin.forms import PaymentForm
from knpay_plugin.views import BaseCompletedView, CreatePaymentMixin

from crud.forms import SignUpForm, UpdateForm
from crud.models import Student, Organization


def home(request):
    return render(request, 'home.html')


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm

    def get_template_names(self):
        if self.request.GET.get('update'):
            self.template_name = 'update.html'
            return self.template_name
        return self.template_name

    def get_form_class(self):
        if self.request.GET.get('update'):
            return UpdateForm

        return self.form_class

    def get_initial(self):
        if self.request.GET.get('update'):
            initial = super().get_initial()
            initial['first_name'] = self.request.user.first_name
            initial['last_name'] = self.request.user.last_name
            initial['dob'] = self.request.user.student.dob
            initial['address'] = self.request.user.student.address
            initial['email'] = self.request.user.email
            initial['contact'] = self.request.user.student.contact
            initial['display_pic'] = self.request.user.student.display_pic
            return initial

    @transaction.atomic
    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        address = form.cleaned_data['address']
        display_pic = form.cleaned_data['display_pic']
        contact = form.cleaned_data['contact']
        email = form.cleaned_data['email']
        dob = form.cleaned_data['dob']
        if self.request.GET.get('update'):
            user = self.request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            student = user.student
            student.address = address
            student.dob = dob
            student.display_pic = display_pic
            student.contact = contact
            student.save()
            return HttpResponseRedirect(reverse('student_detail'))
        else:
            enrollment_no = form.cleaned_data['enrollment_no']
            password = form.cleaned_data['password']
            user = User(username=enrollment_no, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            # dob = datetime.strptime(str(dob), "%m/%d/%Y").strftime("%Y-%m-%d")
            student = Student(user=user, enr_no=enrollment_no, address=address, display_pic=display_pic, dob=dob,
                              contact=contact)
            student.save()
            return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            orgs = Organization.objects.all()
            return render(request, 'student_detail.html', {'orgs': orgs})
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})


def logout(request):
    auth_logout(request)
    return redirect('home')


def student_detail(request):
    return render(request, 'student_detail.html')


def create_fee(request):
    return None


def list_student(request):
    users = User.objects.all()
    students = Student.objects.all()
    return render(request, 'list_student.html', {'users': users, 'students': students})


