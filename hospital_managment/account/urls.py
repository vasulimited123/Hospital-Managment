# """Hospital_Mng_sys URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('signup/', views.signup, name='signup'),
    path('addPatient/', views.addPatient, name='addPatient'),
    path('patientDetails/', views.patientDetails, name='patientDetails'),
    path('changePassword/<user_username>/', views.changePassword, name='changePassword'),
    path('edit_patient/<int:user_id>/', views.edit_patient , name='edit_patient'),
    path('delete_patient/<int:user_id>/', views.delete_patient , name='delete_patient'),
    path('forgot_password/', views.forgot_password , name='forgot_password'),
    path('mail_chng_psd/<str:auth_token>/', views.mail_chng_psd , name='mail_chng_psd'),
]
