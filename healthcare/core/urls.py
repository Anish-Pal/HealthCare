from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser , name='logout'),
    path('signup/',views.signup_start , name='signup'),
    path('verify-otp/' , views.verify_otp , name='verify'),
    path('resened-otp', views.resend_otp , name='resend-otp'),
    path('',views.home , name='home'),
    path('hospitals/', views.hospitals, name='hospitals'),
    path('departments/',views.departments,name='departments'),
    path('doctors/<int:department_id>/',views.doctors,name='doctors'),
    path('chatbot/', views.chatbot_response , name='chatbot_response')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)