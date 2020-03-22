from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class MiximV(LoginRequiredMixin):
    title = ""

    def get_context_data(self,**kwargs):
        context = super(MiximV,self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
