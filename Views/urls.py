from django.contrib import admin
from django.urls import path
from .dasboard_views import AvtorDashbourd ,HubDashbourd, MenegerDashbourd
from .autch_views import Login,Logout
from .ticker_crud_view import TicketCreateView, TicketDeleteView, TicketUpdateView
from .chat_views import TicketDetail ,TicketChatView


urlpatterns = [        
    path('logout/', Logout.as_view(), name="logout"),
    path('login/', Login.as_view(), name="login"),
    
    path('ticket/create/', TicketCreateView.as_view(), name="ticket_form_create"),
    path('ticket/details/<int:pk>/', TicketDetail.as_view(), name='ticket_detail'),

    path('chat/<int:pk>/', TicketChatView.as_view(),
            name='ticket_chats_view'),
    path('update/<int:pk>/', TicketUpdateView.as_view(),
            name='ticket_form_update'),
    path('delete/<int:pk>/', TicketDeleteView.as_view(),
            name='ticket_form_delete'),

    path('autor/', AvtorDashbourd.as_view(), name='user_list'),
    path('maneger/', MenegerDashbourd.as_view(), name='maneger_list'),
    path('', HubDashbourd.as_view(), name='dash_bourd_page'),
]
