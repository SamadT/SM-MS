from lib2to3.fixes.fix_input import context
from os.path import exists

from aiohttp.web_response import Response
from django.contrib.auth import login
from django.db.models import QuerySet
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, HttpResponse
# from pyasn1_modules.rfc3279 import gnBasis
# from pyasn1_modules.rfc5280 import postal_code
from django.forms.models import model_to_dict


from . import forms
from .models import users, user_info, grants, organisations, organisation_needs, join_requests
from django.views import generic
from django.contrib import messages
import datetime
import logging
import ast

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

def sort_cookies(request, info, response):
    try:
        accounts = ast.literal_eval(request.COOKIES.get('account_cookie'))
        # logger.info(accounts)
        for key in accounts.keys():
            accounts[key] = False
        user = info.get("login")
        if user in accounts.keys():
            accounts[user] = True
        else:
            accounts.update({user: True})
        response.set_cookie('account_cookie', accounts)
        return response
    except:
        response.set_cookie('account_cookie', {info.get("login"): True})
        return response

class Authorasation(generic.FormView):
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def get_queryset(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        if users.objects.filter(first_login_ip=ip_address, last_login_ip=ip_address) or users.objects.filter(login=request.COOKIES.get("account_cookie")):
            return HttpResponseRedirect('/')

    def get_pk_name(self, context):
        if self.kwargs.get('pk') == 'sign_up':
            context['link_name'] = 'log_in'
        else:
            context['link_name'] = 'sign_up'
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return self.get_pk_name(context)

    def get_form_class(self):
        pk = self.kwargs.get('pk')
        if pk == 'sign_up':
            form_one = forms.Sign_up_form
            return form_one
        elif pk == 'log_in':
            form_two = forms.Authorisation_form
            return form_two



    template_name = "mergeservice/Authorisation.html"
    #success_url = '/'

    def post(self, request, *args, **kwargs):
        """


        Change cookies to
        dict {"name": False/True - activated}
        Read more about signed cookies next time!

        """
        response = HttpResponseRedirect('/')
        form = self.get_form()
        #logger.warning(form)
        #templ_name = reverse('mergeservice:Authorasation')
        if self.kwargs.get('pk') == 'log_in':
            if form.is_valid():
                ip_address = request.META.get('REMOTE_ADDR')
                info = form.cleaned_data
                #form.clean()
                # if users.objects.filter(first_login_ip=ip_address, last_login_ip=ip_address) or users.objects.filter(login=request.COOKIES.get("account_cookie")):
                if users.objects.filter(name=info.get('First_name'), last_name=info.get('Last_name'), login=info.get('login'), password=info.get('password')):
                    #form.save()
                    """
                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    """
                    users.objects.filter(login=info.get('login')).update(last_login_ip=ip_address)
                    return sort_cookies(request, info, response)
                else:
                    messages.error(request, "There was an error with your form.")
                    return render(request, 'mergeservice/Authorisation.html', {'link_name':"sign_up", 'form':form})
                    #return Response({'link_name':"log_in", 'form':form})
        elif self.kwargs.get('pk') == 'sign_up':
            if form.is_valid():
                ip_address = request.META.get('REMOTE_ADDR')
                #     if not (users.objects.filter(first_login_ip=ip_address, last_login_ip=ip_address) or users.objects.filter(login=request.COOKIES.get("account_cookie"))):
                info = form.cleaned_data
                form.clean()
                #name=info.get('First_name'), last_name=info.get('Last_name'), password=info.get('password') - DELETED
                if not users.objects.filter(login=info.get('login')):
                    users.objects.create(name=info.get('First_name'), last_name=info.get('Last_name'), login=info.get('login'), password=info.get('password'), first_login_ip=ip_address, last_login_ip=ip_address, created_at=datetime.datetime.today().strftime('%d-%m-%Y'))
                    main_user = users.objects.get(login=info.get('login'))
                    user_info.objects.create(address=info.get('address'), city=info.get('city'), postal_code=info.get('postal_code'), administrative_unit=info.get('administrative_unit'), build_number=info.get('build_number'), flat_number=info.get('flat_number'), birth_date=info.get('birth_date'), users_id=main_user)
                    return sort_cookies(request, info, response)
                else:
                    messages.error(request, "That user exists, try to log in!")
                    return render(request, 'mergeservice/Authorisation.html', {'link_name': "log_in", 'form': form})

            #Add invalid form

            #     else:
            #         messages.error(request, "There was an error with your form.")
            # # else:
            #     self.send_problem_mess()
        # return render(request, templ_name, {'form': form})
        #return redirect(f"/authorisation/{self.kwargs.get('pk')}/"))

        #return render(request, 'mergeservice/authorisation.html', {"form": form, 'link_name': ['log_in' if self.kwargs.get('pk') == 'sign_up' else 'sign_up'][0]})
                # context = super().get_context_data()
                # context['problem_message'] = 'Hallo! Deutsch?'
                # return context


class Main_page(generic.ListView):
    template_name = "mergeservice/main_page.html"
    context_object_name = 'grants'

    def seperate_prof_companies(self):
        dict_1 = {}
        for i in list(organisations.objects.filter(org_status=1, rendered=1).values()):
            dict_1.update({i.get('name'): [i.get("description"), i.get("address"), i.get("city")]})
        #logger.info(dict_1)
        return dict_1

    def seperate_non_prof_companies(self):
        dict_1 = {}
        for i in list(organisations.objects.filter(org_status=2, rendered=1).values()):
            dict_1.update({i.get('name'): [i.get("description"), i.get("address"), i.get("city")]})
        #logger.info(dict_1)
        return dict_1


    def get(self, request):
        db_execution = {}
        ip_address = request.META.get('REMOTE_ADDR')
        response = HttpResponseRedirect('/')
        def exctract_cookies(name: str):
            try:
                returned_data = ast.literal_eval(request.COOKIES.get(name))
                return returned_data
            except:
                return None
        accounts = exctract_cookies('account_cookie')
        key_value = ''
        if accounts:
            for key, value in accounts.items():
                if value == True:
                    try:
                        db_execution = users.objects.get(login=key)
                        key_value = key
                        break
                    except:
                        continue
            if db_execution:
                model_dict = model_to_dict(db_execution)
                if model_dict.get('first_login_ip') == ip_address or model_dict.get('last_login_ip') == ip_address:
                    logging.error(list(organisations.objects.values()))

                    return render(request, 'mergeservice/main_page.html', {'grants': grants.objects.values(), 'orgs_prof': self.seperate_prof_companies(), 'orgs_non_prof': self.seperate_non_prof_companies()})
                else:
                    # sort_cookies(request=request, info={'login': key_value}, response=response)
                    users.objects.filter(login=key_value).update(last_login_ip=ip_address)
                    return response
            else:
                return HttpResponseRedirect('/authorisation/sign_up/')
        else:
            return HttpResponseRedirect('/authorisation/sign_up/')
            # db_execution = users.objects.get(first_login_ip=ip_address, last_login_ip=ip_address)
            # logger.warning(db_execution)
        #logger.info(db_execution.get('login'))
        #if db_execution or users.objects.filter(login=request.COOKIES.get("account_cookie")):
        #return render(request, 'mergeservice/main_page.html', {'Halo': 'Halo!'},)
        # else:
        #     return HttpResponseRedirect('/authorisation/log_in/')

    # def get_queryset(self):
    #     context = super().get_context_data()
    #     dict_1 = {}
    #     logging.error(organisation_needs.objects.all().first())
            # grants.objects.

        #return grants.objects.all()

    def post(self, request, *args, **kwargs):
        #logger.warning(request.POST)
        if "_about_us" in request.POST:
            #logger.warning(model_to_dict(users.objects.all()))
            return HttpResponseRedirect('/about_us/')
        list_with_comp_names = organisations.objects.all().values("name")
        for i in [i.get('name') for i in list(list_with_comp_names)]:
            if f"connect_to_{i}" in request.POST:
                # logger.warning(model_to_dict(users.objects.all()))
                return HttpResponseRedirect(f'/join/{i}/')




#Read about classes and insert another
class About_us_view(generic.ListView):
    template_name = "mergeservice/about_us.html"
    context_object_name = 'object'

    def get_queryset(self):
        return 'About Us!'

class Company_creating(generic.ListView):
    template_name = "mergeservice/company_creating.html"
    form_class = forms.organisation_create
    def get(self, request):

        ip_address = request.META.get('REMOTE_ADDR')
        response = HttpResponseRedirect('/')

        def exctract_cookies(name: str):
            try:
                returned_data = ast.literal_eval(request.COOKIES.get(name))
                return returned_data
            except:
                return None

        accounts = exctract_cookies('account_cookie')
        key_value = ''
        if accounts:
            for key, value in accounts.items():
                if value == True:
                    try:
                        db_execution = users.objects.get(login=key)
                        key_value = key
                        break
                    except:
                        continue
            if db_execution:
                model_dict = model_to_dict(db_execution)
                if model_dict.get('first_login_ip') == ip_address or model_dict.get('last_login_ip') == ip_address:
                    return render(request, self.template_name, {'form': self.form_class})
                else:
                    # sort_cookies(request=request, info={'login': key_value}, response=response)
                    users.objects.filter(login=key_value).update(last_login_ip=ip_address)
                    return response
            else:
                return HttpResponseRedirect('/authorisation/sign_up/')
        else:
            return HttpResponseRedirect('/authorisation/sign_up/')

    def end_with_error_messege(self, request, form):
        messages.error(request, "That user exists, try to log in!")
        return render(request, 'mergeservice/company_creating.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.organisation_create(request.POST)
        if form.is_valid():
            ip_address = request.META.get('REMOTE_ADDR')
            info = form.cleaned_data
            form.clean()
            main_user = users.objects.get(login=str([key for key, value in ast.literal_eval(request.COOKIES.get('account_cookie')).items() if value == True])[2:-2])
            #logger.error(info.get('name'), info.get('address'), info.get('city'), info.get('postal_code'), info.get('administrative_unit'), info.get('mail'), info.get('flat_number'), info.get('nip'), info.get('krs'), info.get('description'), main_user)
            #logger.warning(users)
            info.update({"owner":main_user})
            def organisation_check(dictionary):
                temperate_dict = {}
                for key, value in dictionary.items():
                    temperate_dict[key] = value
                    if organisations.objects.filter(**temperate_dict):
                        #logger.error(temperate_dict)
                        #logger.info(organisations.objects.values("name", "address", "city", "postal_code", "administrative_unit", "flat_number", "nip", "krs", "description", "mail").filter(**temperate_dict))
                        return True
                return False
            if organisation_check(info) == False:
                organisations.objects.create(name=info.get('name'), address=info.get('address'), city=info.get('city'), postal_code=info.get('postal_code'), administrative_unit=info.get('administrative_unit'), mail=info.get('mail'), flat_number=info.get('flat_number'), nip=info.get('nip'), krs=info.get('krs'), description=info.get('description'), owner=info.get('owner'))
                return HttpResponseRedirect('/')
            else:
                return self.end_with_error_messege(request, form)
        else:
            return self.end_with_error_messege(request, form)

class Company_cabinet(generic.DetailView):

    def get_queryset(self):
        return None

class Join_company(generic.ListView):
    context_object_name = 'org_name'
    #model = join_requests
    template_name = 'mergeservice/join_form_page.html'
    form_class = forms.org_join

    def get_queryset(self):
        return self.kwargs.get('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = self.form_class
        return context

    def end_with_success_messages(self, request, form):
        messages.success(request, 'We,ve sent your request!!!! Success!!!!')
        return render(request, 'mergeservice/join_form_page.html', {'form': form})

    def end_with_error_messages(self, request, form):
        messages.error(request, "It's fucked up :(\n#ERROR#")
        return render(request, 'mergeservice/join_form_page.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.org_join(request.POST)
        logger.info('asda')
        if form.is_valid():
            logger.info('fghfhdg')
            info = form.cleaned_data
            form.clean()
            main_user = users.objects.get(login=str([key for key, value in ast.literal_eval(request.COOKIES.get('account_cookie')).items() if value == True])[2:-2])
            org=organisations.objects.get(name=self.kwargs.get('pk'))
            logger.info(main_user)
            info.update({"user": main_user, 'org': org})
            if not join_requests.objects.filter(user=info.get('user'), organisation=info.get('org')):
                join_requests.objects.create(email=info.get('email'), user=info.get('user'), organisations=info.get('org'), description=info.get('description'), phone_number=info.get('phone_number'))
                return self.end_with_success_messages(request, form)
        return self.end_with_error_messages(request, form)

    # def post(self, request, *args, **kwargs):
    #     if self.form_class.is_valid():

    # def form_valid(self, form):
    #     form.save()
    #     return HttpResponseRedirect('/')

    # def post(self, request):
    #     list_with_comp_names = organisations.objects.all().values("name")
    #     logger.warning(list_with_comp_names)
    #     if "connect_to_" in request.POST:
    #         #logger.warning(model_to_dict(users.objects.all()))
    #         return HttpResponseRedirect(f'/{request.POST.replace("connect_to_", "join/")}/')



class Grant_creating():

    def get_queryset(self):
        return None
