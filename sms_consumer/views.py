import django
from django.db.models.aggregates import Count
from django.shortcuts import render
from django.views.generic import View
from .models import *
from .forms import *
import pdb
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse

class SmsLog(View):
    def get(self, request):
        user = SmsLogModel.objects.all()
        return render(request=request, template_name='sms_consumer/msg.html', context={'user':user})


    def post(self, request):
        ms = request.POST.get('message')
        for i in request.POST.getlist('contact_no'):
            reg = SmsLogModel(user_id=1, message=ms,count=1,contact_no = i)
            pdb.set_trace()
            reg.save()
        return render(request, 'sms_consumer/msg.html')


class ConsumerList(View):
    def get(self, request):
        user = SmsUser.objects.all()
        # pdb.set_trace()
        smform = SmsConsumerForm()
        return render(request=request, template_name="sms_consumer/addcount.html", context={"user":user, "smform":smform})

    # def post(self, request):
    #     ct = int(request.POST.get('sms'))
    #     fm = SmsUser.objects.get(id=2)
    #     gm = fm.sms_count + ct
    #     cs = SmsUser(sms_count = gm)
    #     pdb.set_trace()
    #     cs.save()
    #     return HttpResponse("succesfull adding the sms")
    # def get_absolute_url(self):
    #      return reverse('/count', args=(str(self.id)))

class ConsumerUpdate(View):
    def post(self, request):
        ct = int(request.POST.get('sms'))
        fm = SmsUser.objects.get(id=2)
        gm = fm.sms_count + ct
        cs = SmsUser(sms_count = gm)
        pdb.set_trace()
        cs.save()
        return HttpResponse("succesfull adding the sms")
    def get_absolute_url(self):
         return reverse('countupdate', args=(str(self.id)))


    