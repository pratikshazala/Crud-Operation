from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Submit
from django import forms
from django.urls import reverse
from crud import views


class CommonForm(forms.Form):
    first_name = forms.CharField(max_length=10, required=True)
    last_name = forms.CharField(max_length=10, required=False)
    dob = forms.DateField(widget=forms.TextInput(
        attrs={'type': 'date'}
    ), help_text='Format : DD/MM/YYYY')
    # dob = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y'), help_text='Format : DD/MM/YYYY')
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), required=False)
    display_pic = forms.ImageField()
    contact = forms.CharField(max_length=15)
    email = forms.EmailField()


class SignUpForm(CommonForm):
    enrollment_no = forms.CharField(max_length=12, required=True)
    password = forms.CharField(min_length=6, max_length=16, widget=forms.PasswordInput())
    confirm_password = forms.CharField(min_length=6, max_length=16, widget=forms.PasswordInput(), help_text='Enter password same as entered before')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = "POST"
    #     # self.helper.form_action = reverse(views.login)
    #     self.helper.layout = Layout(
    #         Row(Column('enrollment_no', css_class='form-group col-md-6 mb-0')),
    #         Row(
    #             Column('first_name', css_class='form-group col-md-6 mb-0'),
    #             Column('last_name', css_class='form-group col-md-6 mb-0')
    #         ),
    #         Row(
    #             Column('address', css_class='form-group col-md-6 mb-0'),
    #             Column('display_pic', css_class='form-group col-md-6 mb-0')
    #         ),
    #         Row(
    #             Column('contact', css_class='form-group col-md-4 mb-0'),
    #             Column('email', css_class='form-group col-md-4 mb-0'),
    #             Column('dob', css_class='form-group col-md-4 mb-0 mb-0')
    #         ),
    #         Row(
    #             Column('password', css_class='form-group col-md-6 mb-0'),
    #             Column('confirm_password', css_class='form-group col-md-6 mb-0'),
    #             css_class='pb-3'
    #         ),
    #         Submit('submit', 'Sign Up')
    #     )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        first_name = cleaned_data.get('first_name')
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', 'Password does not match.')

        if len(first_name) < 3:
            self.add_error('first_name', 'Please specify valid name')


class UpdateForm(CommonForm):
    pass