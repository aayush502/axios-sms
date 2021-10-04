from django.db.models.aggregates import Count
from django.db.models.query import InstanceCheckMeta
from django.http import request
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from .models import *
from .forms import *
import pdb
from django.http.response import HttpResponse, HttpResponseRedirect


class SmsLog(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect("login")
        else:
            user_id=request.session['user_id']
            sms_user = SmsUser.objects.get(id=user_id)
            if sms_user.is_admin:
                user = SmsLogModel.objects.all()
                current_user = SmsUser.objects.filter(id=request.session["user_id"])[0]
                return render(request=request, template_name='sms_consumer/msg.html', context={'user':user, 'current_user':current_user})
            else:
               return HttpResponse("You are not an authorized user.")

    def post(self, request):
        ms = request.POST.get('message')
        user_id = request.session['user_id']
        msg_count = request.POST.get('message_count')
        lesscount=0
        smuser_user = SmsUser.objects.get(id=user_id)
        counter = smuser_user.sms_count
        for i in request.POST.getlist('contact_no'):
            reg = SmsLogModel(user_id=user_id, message=ms,count=msg_count,contact_no = i)
            reg.save()
            lesscount += int(reg.count)
        count = counter-lesscount
        SmsUser.objects.filter(id=user_id).update(sms_count = count)
        # user tabke ko count -lesscoune ani save
        return redirect('/log') 



class ConsumerList(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect("/login")
        else:
            user_id=request.session['user_id']
            sms_user = SmsUser.objects.get(id=user_id)
            if sms_user.is_admin:
                user = SmsUser.objects.all()
                return render(request, template_name="sms_consumer/addcount.html", context={"user":user})
            else:
                return HttpResponse("you are not an authorized user")

class ConsumerUpdate(View):
    def post(self, request, id):
        ct = int(request.POST.get('sms'))
        fm = get_object_or_404(SmsUser, id=id)
        fm.sms_count = fm.sms_count+ct
        fm.save()
        return redirect("count")
    


class UserRegister(View):
    def get(self, request):
        return render(request, template_name="registration/register.html", context={})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('pass')
        sms_count = int(request.POST.get('number'))
        try:
            SmsUser.objects.get(email=email)
            return HttpResponse('Email already exists')
        except SmsUser.DoesNotExist:
            reg = SmsUser.objects.create(email = email, password = password, sms_count = sms_count)
            subject = "You have been registered in axios-sms"
            message = 'registration successful'
            try:
                get_mail = reg.email
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [get_mail])
                return render(request, template_name="mailer/mailer.html", context={"user":get_mail} )
            except BadHeaderError:
                    return HttpResponse('Invalid header found.')

class UserLogin(View):
    def get(self, request):
        return render(request, template_name="registration/login.html",context={})

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("pass")
        smsuser = SmsUser.objects.filter(email=email,password=password)
        for user in smsuser:
            password = user.password
            if password == request.POST.get('pass'):
                request.session['user_id'] = user.id
                return redirect("home")    
        return HttpResponse("username or password donot match")

def logout(request):
    try:
        del request.session['user_id']
    except:
        return redirect('login')
    return redirect('login')

class Home(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('/login')
        else:
            user = request.session['user_id']
            sms_user = SmsUser.objects.get(id=user)
            return render(request, template_name="base.html", context={"user":sms_user, "user_id":user})