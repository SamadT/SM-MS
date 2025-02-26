from cProfile import label

from django import forms
from django.forms.models import model_to_dict
from phonenumber_field.modelfields import PhoneNumberField
from . import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

from . import views


class Sign_up_form(forms.Form):
    First_name = forms.CharField(max_length=50, required=True, label='First name')
    Last_name = forms.CharField(max_length=60, required=True, label='Last name')
    login = forms.CharField(max_length=60, required=True, label='Login')
    password = forms.CharField(max_length=60, required=True, label='Password', widget=forms.PasswordInput)
    address = forms.CharField(max_length=90, label='Address')
    city = forms.CharField(max_length=7, label="City", required=True)
    postal_code = forms.CharField(max_length=10, label="Postal code")
    administrative_unit = forms.CharField(max_length=30, label='Administrative unit')
    build_number = forms.CharField(max_length=10, required=10, label='Build number')
    flat_number = forms.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(2000)
    ])
    birth_date = forms.DateField(help_text='Your birthday(dd/mm/yyyy)', validators=[
            MinValueValidator(datetime.date(day=1, month=1, year=1700)),  # Minimum date: Jan 1, 2023
            MaxValueValidator(datetime.date(day=31, month=12, year=2024)),  # Maximum date: Dec 31, 2023
        ], widget=forms.TextInput(attrs={'type': 'date'}), label="Birth date")

class Authorisation_form(forms.Form):
    First_name = forms.CharField(max_length=50, required=True, label='First name')
    Last_name = forms.CharField(max_length=60, required=True, label='Last name')
    login = forms.CharField(max_length=60, required=True, label='Login')
    password = forms.CharField(max_length=60, required=True, label='Password', widget=forms.PasswordInput)


class organisation_create(forms.Form):
# class organisation_create(forms.ModelForm):
    name = forms.CharField(max_length=75, required=True, label="Org. Name")
    address = forms.CharField(max_length=90, label='Main office address(or )')
    city = forms.CharField(max_length=25)
    postal_code = forms.CharField(max_length=10)
    administrative_unit = forms.CharField(max_length=50, required=True)
    mail = forms.EmailField(required=True, max_length=100, label='Email')
    flat_number = forms.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(2000)
    ])
    nip = forms.IntegerField(required=True)
    krs = forms.IntegerField(required=True)
    description = forms.CharField(max_length=1000, widget=forms.Textarea, required=True)
    # class Meta:
    #     model = models.organisations
    #     fields = ["name", "address", "city", "postal_code", "administrative_unit", "mail", "flat_number", "nip", "krs", "description", "owner"]

class org_join(forms.ModelForm):
    # first_name = forms.CharField(max_length=50, required=True, label="First name")
    # surname = forms.CharField(max_length=60, required=True, label="Surname")



    # description = forms.CharField(max_length=1000, widget=forms.Textarea, required=True)
    # phone_number = PhoneNumberField()
    # class Meta:
    #     model = models.join_requests
    #     fields= ["user", "organisation", "description", "phone_number"]
    email = forms.EmailField(max_length=150, required=True, label="email")
    description = forms.CharField(max_length=1000, widget=forms.Textarea, required=True)
    phone_number = PhoneNumberField()
    class Meta:
        model = models.join_requests
        fields= ["email", "description", "phone_number"]



    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Customize author field if needed
    #     self.fields['owner'].queryset = models.users.objects.values('name')
    #     views.logger.info(model_to_dict(models.users.objects.values('name')))

    # def get_current_form_object(self, form_name):
    #     if form_name == "sign_up":
    #         form = Sign_up_form
    #         with open("you.txt", "w+") as gfg_file:
    #             gfg_file.write(form)
    #     elif form_name == "log_in":
    #         form = Authorisation_form
    #         with open("you.txt", "w+") as gfg_file:
    #             gfg_file.write(form)
    #     return form

# def get_current_form_object(form_name, *form_object):
#     if form_name == "sign_up":
#         form = Sign_up_form
#         with open("you.txt", "w+") as gfg_file:
#             gfg_file.write(form)
#         form_object = form
#     elif form_name == "log_in":
#         form = Authorisation_form
#         form_object = form
#         with open("you.txt", "w+") as gfg_file:
#             gfg_file.write(form)
#     return form_object
