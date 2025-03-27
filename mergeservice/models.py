# from email.policy import default
# from operator import truediv
# from tkinter.font import names

# from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import admin
from phonenumber_field.modelfields import PhoneNumberField
"""
users name, lastname, login, password, accesslevel (smallint -1, 0, 1), first_login_ip, last_login_ip, created_at, deleted_at
user_info address, city, postal_code, administrative_unit, build_number, flat_number, birth_date 
user_types organisation_id, name
join_requests id_user, organisation_id, description
organisations – is_non_profit, name, address, city, postal_code, administrative_unit, build_number, flat_number, nip, krs(nullable), description, 
grants – organisation_id, description, sum_value, currency(default – “pln”), created_at
closed_at(null default), receiver_organisation_id – receiver
grant_applications  organisation_id, description, grant_id, created_at
organisation_categories id, name (animal, kids, other, flood)
organisation_types organisation_id, organisation_category_id
organisation_needs organisation_id, description, sum_value, currency(default – “pln”), is_closed, organisation_relised_id 
organisation_users -  id_user, id organisation, 
organisation_user_types - user_id user_type_id
"""

class users(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=60)
    login = models.CharField(max_length=60)
    password = models.CharField(max_length=20)
    accesslevel = models.SmallIntegerField(default=0)
    first_login_ip = models.CharField(max_length=15)
    last_login_ip = models.CharField(max_length=15)
    created_at = models.CharField(max_length=12)
    deleted_at = models.CharField(max_length=12, null=True)

class user_info(models.Model):
    users_id = models.ForeignKey(users, on_delete=models.CASCADE)
    address = models.CharField(max_length=90, null=True)
    city = models.CharField(max_length=7)
    postal_code = models.CharField(max_length=10, null=True)
    #Mazowieckie, Łódzkie
    administrative_unit = models.CharField(max_length=30, null=True)
    build_number = models.CharField(max_length=10, null=True)
    #!!!!!!!!!!!!!!
    flat_number = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(2000)
    ], null=True)
    #birth_date = models.DateField(null=True, input_formats=settings.DATE_INPUT_FORMATS)
    birth_date = models.DateField(null=True)

class organisations(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=90, null=True)
    city = models.CharField(max_length=7, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    administrative_unit = models.CharField(max_length=50, null=True)
    #!!!!!!!!!!!!!!!!!!!
    flat_number = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(2000)
    ])
    nip = models.IntegerField()
    krs = models.IntegerField()
    description = models.TextField(max_length=1000)
    org_status = models.SmallIntegerField(default=0)
    rendered = models.BooleanField(default=False)
    mail = models.CharField(max_length=100)
    owner = models.ForeignKey(users, on_delete=models.CASCADE)

    @admin.display(
        boolean=True,
        ordering="rendered",
        description="If rendered?"
    )
    def __str__(self):
        return f"{self.name} - {self.address} - {self.city} - {self.postal_code} - {self.administrative_unit} - {self.description} - {self.mail}"

# class user_types(models.Model):
#     organisations = models.ForeignKey('organisations', on_delete=models.CASCADE)
#     description = models.TextField(max_length=1000)

class join_requests(models.Model):
    email = models.EmailField(max_length=150)
    user = models.ForeignKey('users', on_delete=models.CASCADE)
    organisation = models.ForeignKey('organisations', on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    phone_number = PhoneNumberField(max_length=15)

    # def __str__(self):
    #     return self.organisation

class grants(models.Model):
    organisations = models.ForeignKey('organisations', on_delete=models.CASCADE, related_name='org_id')
    description = models.TextField(max_length=1000)
    sum_value = models.IntegerField()
    currency = models.CharField(max_length=3)
    created_at = models.DateField()
    closed_at = models.DateField(null=True)
    receiver_organisation_id = models.ForeignKey('organisations', on_delete=models.CASCADE, related_name='organisations_id', null=True)
    #receiver

# class grant_applications(models.Model):
#     organisations = models.ForeignKey('organisations', on_delete=models.CASCADE)
#     description = models.TextField(max_length=1000)
#     grant_id = models.ForeignKey('grants', on_delete=models.CASCADE)
#     created_at = models.DateField()

# class organisation_categories(models.Model):
#     name = models.CharField(max_length=50)

# class organisation_types(models.Model):
#     organisations = models.ForeignKey('organisations', on_delete=models.CASCADE)
#     organisation_categories = models.ForeignKey('organisation_categories', on_delete=models.CASCADE)

class organisation_needs(models.Model):
    organisations = models.ForeignKey('organisations', on_delete=models.CASCADE, related_name='organ_id')
    description = models.TextField(max_length=1000)
    sum_value = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    currency = models.CharField(max_length=3)
    is_closed = models.BooleanField(default=False)
    organisation_relised_id = models.ForeignKey('organisations', on_delete=models.CASCADE, related_name='relised_org_id')

class organisation_users(models.Model):
    users = models.ForeignKey('users', on_delete=models.CASCADE)
    status_level_in_organisation = models.SmallIntegerField(default=0)
    organisation = models.ForeignKey('organisations', on_delete=models.CASCADE)

# class organisation_user_types(models.Model):
#     users = models.ForeignKey('users', on_delete=models.CASCADE)
#     user_types = models.ForeignKey('user_types', on_delete=models.CASCADE)