import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from Base.models import TicketBD

logger = logging.getLogger(__name__)

class AbstractDashBourd(LoginRequiredMixin, ListView):
    template_name = "label/dashBoard.html"
    model = TicketBD
    context_object_name = 'dash'
    alert_str = None
    title = "Dasboard"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["alert_str"]=self.alert_str
        context['title']=self.title
        return context

class HubDashbourd(AbstractDashBourd):
    alert_str = "Групповые заявки."

    def get_queryset(self):
        q = self.model.objects.get_group_article(self.request.user)
        return q

class AvtorDashbourd(AbstractDashBourd):
    alert_str="Созданные заявки пользователя."

    def get_queryset(self):
        q = self.model.objects.get_article_user_autor(self.request.user)
        return q

class MenegerDashbourd(AbstractDashBourd):
    alert_str="Заявки под управлениям пользователя."

    def get_queryset(self):
        q = self.model.objects.get_article_user_maneger(self.request.user)
        return q
