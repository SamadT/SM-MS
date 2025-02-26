from django.urls import path
from . import views

app_name = "mergeservice"
urlpatterns = [
    path("authorisation/<str:pk>/", views.Authorasation.as_view(), name="Authorasation"),
    path("", views.Main_page.as_view(), name="Main_page"),
    path("about_us/", views.About_us_view.as_view(), name="About_us_view"),
    path("company_creating/", views.Company_creating.as_view(), name="Company_creating"),
    path("company_cabinet/<str:pk>/", views.Company_cabinet.as_view(), name='Company_cabinet'),
    path("join/<str:pk>/", views.Join_company.as_view(), name='Join_company')
]