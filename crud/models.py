from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django_extensions.db.models import TimeStampedModel, ActivatorModel


class Student(TimeStampedModel, ActivatorModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    enr_no = models.CharField('Enrollment No', primary_key=True, max_length=12)
    dob = models.DateField()
    display_pic = models.ImageField(upload_to='img/')
    address = models.TextField()
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class Organization(TimeStampedModel, ActivatorModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    contact = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Course(TimeStampedModel, ActivatorModel):
    organization = models.ManyToManyField('Organization')
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Fees(TimeStampedModel):
    fee = models.CharField(max_length=7)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.fee


class Transaction(TimeStampedModel, ActivatorModel):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=50)
    order_id = models.CharField(max_length=15)
    amount = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=25)
    m_id = models.CharField(max_length=22)

    def __str__(self):
        return self.user
