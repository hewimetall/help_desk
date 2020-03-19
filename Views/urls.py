from django.contrib import admin
from django.urls import path,include,re_path
from .dasboard_views import AvtorDashbourd ,HubDashbourd, MenegerDashbourd
from .autch_views import Login,Logout

urlpatterns = [        
    path('logout/', Logout.as_view(), name="logout"),
    path('login/', Login.as_view(), name="login"),
    path('login/', Login.as_view(), name="ticketForm_create"),
    
    re_path(r'^autor/', AvtorDashbourd.as_view(), name='UserList'),
    re_path(r'^maneger/', MenegerDashbourd.as_view(), name='ManegerList'),
    path('', HubDashbourd.as_view(), name='dashBourdPage'),
]
