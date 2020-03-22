from django.contrib import admin
from django.urls import path,include
from .views import RestChatUpdate, ChatUserList, DetailTicket


urlpatterns = [

    path('chat_form/<int:pk>/',
            RestChatUpdate.as_view(), name='chat_user_update'),
    path('chat_list/<int:pk>',
            ChatUserList.as_view(), name='chat_user_list'),
    path('ticket_details/<int:pk>',
            DetailTicket.as_view(), name='ticket_details'),

]
