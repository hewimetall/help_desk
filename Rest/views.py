from django.http.response import Http404, HttpResponse
from django.views.generic import View
from Base.models import TicketBD ,TicketChat 
from Forms.forms_chat import TicketChatForm
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize

# Create your views here.
class RestChatUpdate(LoginRequiredMixin,View):
    http_method_names = ['get', 'post', ]
    model = TicketBD
    model2 = TicketChat
    form = TicketChatForm()

    def get(self,request,**kwarg):
        return Http404("Page not faund")

    def post(self, request, *args, **kwargs):
        # get form +
        # valid form +
        # save data +
        # return Okk +
        # print("test 0") +
        obj = self.get_object()
        # print("test 1") +
        form = self.get_form(pk=obj.pk, user=self.request.user)
        # print("test 2") +
        data = self.valid_form_try(form)
        if not hasattr(data,"body"):
            self.push_a()
        # print("test 3") +
        self.save(data["status"], data["body"], data["name"], data["file"])
        # print("test 4") +
        return HttpResponse("ok")

    def get_form(self, pk, user):
        role = self.model.objects.get_role(user=user, pk=pk)
        form = self.form.get_form(role)
        return form

    def get_object(self):
        objects = self.model.objects.get(pk=self.kwargs['pk'])
        return objects

    def valid_form_try(self, form):
        forms = form(self.request.POST or None)
        if not forms.is_valid():
            raise ValueError("form is not  valid")
        if not hasattr(forms,'getSTATUS'):
            return forms.cleaned_data
        data=forms.cleaned_data
        data['name']=self.request.user
        data['status']=forms.getSTATUS(data)
        if not 'file' in data:
            data['file']=None
        return data


    def push_a(self):
            q = self.get_object()
            q.maneger = self.request.user
            q.save()


    def save(self, status, body, name, file):
        if status != None:
            q = self.get_object()
            q.status = status
            q.save()

            q2 = self.model2(post=self.get_object(),
                             name=name, body=body, file=file)
            q2.save()

class ChatUserList(LoginRequiredMixin,View):
    http_method_names = ['get', ]
    field             = ['name','body','updated']
    def get(self, request, *args, **kwargs):
        q=self.get_queryset()
        resp=[]
        for i in q:
            d={}
            for j in self.field:
                if j == "name":
                    name = getattr(i,j).full_name
                    if len(name) == 0 :
                        name = getattr(i,j).username 
                    d[j] = name   
                elif j == "updated":
                    data = getattr(i,j)
                    d[j] = "{}".format(data)       
                else: 
                    d[j] = getattr(i,j)
            resp.append(d)
        return JsonResponse(resp, safe=False)

    def get_queryset(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            tic = TicketBD.objects.filter(pk=pk)
            q = TicketChat.objects.filter(post=tic)
            return TicketChat.objects.all()


class DetailTicket(LoginRequiredMixin,View):
    http_method_names = ['get', ]
    field             = ['name','body','updated']
    def get(self, request, *args, **kwargs):
        q=TicketBD.object.vireficate_art(request.user,kwargs['pk'])
        js=serialize("json",q)
        return JsonResponse(js, safe=False)
