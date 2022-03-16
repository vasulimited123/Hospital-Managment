from audioop import add
import email
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate,logout , get_user_model
from django.contrib.auth.models import User #import user model
from account.models import Patient_Details #impotr Patient_Details model
from django.core.mail import send_mail
import uuid
import datetime




def Home(request):
    return render(request,'header.html')

def addPatient(request):
     if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['user_name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        zip_code = request.POST['zip_code']
        image = request.FILES.get('image')
        user = User.objects.create_user( username = user_name , email = email, first_name = first_name, last_name = last_name )
        Patient_Details.objects.create(user = user, phone = phone, address = address, zip_code = zip_code, image =image)
        messages.success(request, 'Patient Profile Created Sucessfully')
        return redirect('patientDetails')
     return render(request, 'addPatient.html')

def patientDetails(request):
    data = Patient_Details.objects.all().values( 'user__id','user__first_name', 
    'user__last_name', 'user__email', 'address', 'phone', 'zip_code', 'image')
    return render(request,'patient_list.html', {'data': data} )
    

def changePassword(request, user_username):
    if request.method == 'POST':
        password = request.POST['password']
        newPassword = request.POST['newPassword']
        reNewPsd = request.POST['reNewPsd']
        if newPassword == reNewPsd:
            u = User.objects.get(username = user_username)
            if u.check_password(password):        
                u.set_password(newPassword)
                u.save()
                messages.success(request, 'Password Update Successfully')
                logout(request)
                return redirect('login')
            else:
                messages.success(request, 'Password And Old Password Must Be Same')
        else:
            messages.success(request, 'Password Not Match')
    return render(request, 'changePassword.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def login(request):
    if request.method == 'POST':
        mail = request.POST['email']
        password = request.POST['psd']
        if User.objects.filter(username = mail).exists():
            user = authenticate(username = mail, password = password)
            if user is not None:
                # auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('dashboard')
            messages.error(request,'Please enter correct email and password..!')
            return redirect('login')
        messages.error(request,'That email is not registered')
        return redirect('signup')
    return render(request,'login.html')

def userlogout(request):
     logout(request)
     messages.error(request,'Logged Out Sucessfully')
     return redirect('home')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user_name = request.POST['user_name']
        password = request.POST['pds']
        confirm_password = request.POST['Cpds']
        if password == confirm_password:
            if not User.objects.filter(username = user_name ).exists():
                user = User.objects.create_user(password = password, email = email, first_name = first_name, last_name = last_name, username = user_name )
                messages.success(request, 'You are now logged in')
                return redirect('login')
            messages.error(request,'Sorry, this email is already used..!')
            return redirect('signup')
        messages.error(request,'Passwords do not match')
        return redirect('signup')
    return render(request,'singup.html')

def createpat(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user_name = request.POST['user_name']
        password = request.POST['pds']
        confirm_password = request.POST['Cpds']
        phone = request.POST['phone']
        address = request.POST['address']
        zip_code = request.POST['zip_code']
        image = request.FILES.get('image')
        if password == confirm_password:
            if not User.objects.filter(username = user_name ).exists():
                user = User.objects.create_user(password = password, email = email, first_name = first_name, last_name = last_name, username = user_name )
                Patient_Details.objects.create(phone = phone, address = address, zip_code = zip_code, image =image)
                messages.success(request, 'You are now logged in')
                return redirect('login')
            messages.error(request,'Sorry, this email is already used..!')
            return redirect('createpat')
        messages.error(request,'Passwords do not match')
        return redirect('createpat')
    return render(request,'create.html')

def edit_patient(request , user_id):
    patient_data = Patient_Details.objects.get(user_id = user_id)
    if request.method == 'POST':
        phone = request.POST['phone']
        address = request.POST['address']
        zip_code = request.POST['zip_code']
        # image = request.FILES.get('image')
        Patient_Details.objects.filter(user_id = user_id).update(phone = phone, address = address, zip_code = zip_code)
        patient_data = Patient_Details.objects.get(user_id = user_id)
        messages.success(request, 'Update Successfully')
        return redirect('edit_patient', user_id)
    return render(request,'edit.html' , {'patient': patient_data})

def delete_patient(requset , user_id):
    User.objects.filter(id = user_id).delete()
    return redirect('patientDetails')

def forgot_password(request):
    if request.method == 'POST':
        mail = request.POST['mail']
        b = User.objects.filter(email = mail)
        if len(b) <= 0:
            messages.error(request, 'please enter valid emial id')
        else:
            b = User.objects.get(email = mail)
            messages.success(request, 'Email send Successfully')
            auth_token = str(uuid.uuid4())
            forgot_password_time= datetime.datetime.now(datetime.timezone.utc)
            Patient_Details.objects.filter(user_id = b.id).update(auth_token = auth_token, is_link = False, date= forgot_password_time)
            send_email(mail,auth_token)
            return redirect('/mail_chng_psd/{auth_token}/')
    return render(request ,'mail.html')



def send_email(email,auth_token):
    subject = "Mail Regarding Change Password "
    message = f"click to update your password http://127.0.0.1:8000/mail_chng_psd/{auth_token}/"
    email_from = settings.EMAIL_HOST_USER
    rece = [email]
    send_mail(subject, message, email_from, rece)
    


def mail_chng_psd(request, auth_token):
    try:
        u = Patient_Details.objects.get(auth_token = auth_token) 
    except:
        return render(request ,'sendmail.html')
    print(u.is_link)
    u = Patient_Details.objects.get(auth_token = auth_token)
    ct = datetime.datetime.now(datetime.timezone.utc)
    difference = ct - u.date
    difference_hour = difference.total_seconds()  
    if u.is_link == False and difference_hour < 60:
        if request.method == 'POST':
            newPassword = request.POST['newPassword']
            Patient_Details.objects.filter(auth_token = auth_token).update(is_link = True)
            c = User.objects.get(id = u.user_id)       
            c.set_password(newPassword)
            c.save()
            messages.success(request, 'Password Update Successfully')
            logout(request)
            return redirect('login')        
        else:
            return render(request, 'mail_chng_psd.html')
    messages.success(request, 'Link Is Expire')
    return render(request ,'login.html') 