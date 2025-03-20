from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.db import transaction


from .models import *
from .forms import *
from .predict import predict
# from .utils import *
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.db.models import F, Value, IntegerField, Sum,Q,Max
from django.db.models.functions import Cast
from datetime import datetime

from django.conf import settings
import os

# Create your views here.
def index(request):
    return render(request,'index.html')

def logout(request):
    request.session.clear()
    return redirect('index')

def login_view(request):
    return render(request,'auth/login.html')

def register_view(request):
    return render(request,'auth/register.html')

def createAccount(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            response = {
                'status': True,
                'message': 'User Created Successfully'
            }
            return JsonResponse(response)
        else:
            # Form is not valid, extract error messages
            errors = form.errors
            print(errors)
            error_message = str(errors['contact'][0]) if 'contact' in errors else str(errors['email'][0]) if 'email' in errors  else 'Invalid form data'

            response = {
                'status': False,
                'message': error_message
            }
            return JsonResponse(response)
        
    return JsonResponse({ 'status':False, 'message':'Invalid Request Method!' })

def loginAccount(request):
    if request.method=='POST':
        response={
            'status':False,
            'message':'Invalid Request Method!'
        }
           
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.filter(email=email,password=password,is_active=1).first()

        if user is None:
            response={
                'status':False,
                'message':'Invalid User'
            }
        else:
            request.session['userId']=user.id
            request.session['user_type']=user.user_type
            
            response={
                'status':True,
                'message':'Successfully logged in'
            }
           
    return JsonResponse(response)


def home_view(request):
    return render(request,'home/home.html')

def upload(request):
    return render(request,'home/upload.html')

def detect_slide(request):
    if request.method == 'POST':
        # print(request.POST)

        season = request.POST['season']
        moisture = request.POST['moisture']
        type = request.POST['type']
        slope = request.POST['slope']
        stress = request.POST['stress']
        construction = request.POST['construction']
        mining = request.POST['mining']
        deforest = request.POST['deforest']
        location = request.POST['location']
       
        data = [season,moisture,type,slope,stress,construction,mining,deforest]

        result = predict(data)
        message = "Landslide not likely to happen"
        if int(result) == 1:
            message = "Landslide likely to happen"
            sendEmailMessage(location)
        
        return JsonResponse({ 'status':True, 'message':message})
    else:
        return JsonResponse({ 'status':False, 'message':'Invalid Request Method!' })
    
def sendEmailMessage(location):
    predicted_date = datetime.now().strftime("%Y-%m-%d")
    subject = f"Landslide Warning Notification"
    message = f"""
    Urgent: Landslide Warning
    
    Dear Concerned Authorities,

    We are sending you this message to inform you that, based on recent data, there is a high likelihood of a landslide occurring in the affected area. Please take necessary precautions immediately.
    Stay updated with weather reports and landslide alerts.
    Avoid living or staying in landslide-prone areas, such as steep slopes or valleys.
    Look out for warning signs like cracks in the ground, leaning trees, or changes in water flow.
    Prepare an emergency kit with essentials (food, water, flashlight, first aid, and important documents).
    Know evacuation routes and safe zones in your area.
    Inform family and neighbors about the risk and discuss evacuation plans.
    Stay indoors if safe or move to higher, stable ground.
    Protect yourself: if caught, curl into a ball to shield your head and body.
    Details:
    - Location: {location}
    - Predicted Date: {predicted_date}
    - Severity: High

    We urge you to take preventive measures to avoid any unfortunate incidents.

    Stay Safe!

    Best regards,
    The Landslide Monitoring Team
    """

    from_email = 'supportlandslide@gmail.com'
    recipient_list = ['suvarna.thashvy2021@gmail.com']
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)