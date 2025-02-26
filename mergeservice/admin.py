from urllib.parse import uses_query
#from .views import logger

from django.contrib import admin
from .models import users, user_info, organisations, organisation_users

"""
admin
1234
"""
# Register your models here.

class usesrs_inline_info(admin.StackedInline):  # or StackedInline
   model = user_info
   fieldsets = [(None, {"fields": ['address', 'city', 'postal_code', 'administrative_unit', 'build_number', 'flat_number', 'birth_date']})]
   extra = 0

class organisation_users_inline(admin.StackedInline):
    model = organisation_users
    extra = 0

#models_for_user_list = [users, user_info]
class user_list(admin.ModelAdmin):
    inlines = [usesrs_inline_info]
    fieldsets = [("Users", {"fields": [('name', 'last_name'), 'login', 'password', 'accesslevel', ('first_login_ip', 'last_login_ip'), ('created_at', 'deleted_at')]})]
    list_display = ['name', 'last_name', 'login', 'password', 'accesslevel', 'first_login_ip', 'last_login_ip', 'created_at', 'deleted_at']
    #inlines = [users_model, users_info_model]
    # fieldsets = [("Users",
    #               {"fields": [('name', 'last_name'), 'login', 'password', 'accesslevel', ('first_login_ip', 'last_login_ip'), ('created_at', 'deleted_at')]})]
    # list_display = ['name', 'last_name', 'login', 'password', 'accesslevel', 'first_login_ip', 'last_login_ip', 'created_at', 'deleted_at']
    list_filter = ['login']
    search_fields = ['login']
    #readonly_fields = ('password', 'login', 'first_login_ip', 'last_login_ip', 'created_at', 'deleted_at', 'name', 'last_name')
admin.site.register(users, user_list)

class organisation_list(admin.ModelAdmin):
    inlines = [organisation_users_inline]
    fieldsets = [("Organisations", {"fields": ["name", "address", "city", ("postal_code", "administrative_unit"), "flat_number", ("nip", "krs"), "description", ("org_status", "rendered"), "mail", "owner"]})]
    list_display = ["name", "address", "city", "postal_code", "administrative_unit", "flat_number", "nip", "krs", "description", "org_status", "rendered", "mail", "owner"]
    list_filter = ["rendered"]
    search_fields = ["name"]
admin.site.register(organisations, organisation_list)
