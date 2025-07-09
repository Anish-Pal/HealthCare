from django.shortcuts import render , get_object_or_404
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from . models import Hospital
from . models import Bed
from . models import Department
from . models import Doctor , Slot
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect
from django.contrib import messages
import random
from django.core.mail import send_mail
from .models import OTPVerification
from .form import PreSignupform, OTPForm
from django.utils import timezone
from twilio.rest import Client



gen_ai = settings.GEN_AI

# Create your views here.

def send_otp_sms(to_phone, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to = f"+{to_phone}"
    )
    return message.sid


def signup_start(request):
    if request.method == 'POST':
        form = PreSignupform(request.POST)
        if form.is_valid():
            email_or_phone = form.cleaned_data["email_or_phone"]
            full_name = form.cleaned_data["full_name"]
            password = form.cleaned_data["password1"]

            otp = f"{random.randint(100000,999999)}"

            obj, created = OTPVerification.objects.get_or_create(
                           email_or_phone=email_or_phone,
                           defaults={"otp_code": otp}
            )
            if not created:
               obj.otp_code = otp
               obj.created_at = timezone.now()
               obj.save()


            if "@" in email_or_phone:
                send_mail(
                    "Your OTP code",
                    f"Hello {full_name}, your OTP is {otp}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email_or_phone]
                )
            else:
                 sms_number = "91"+email_or_phone
                 send_otp_sms(sms_number,otp)

            request.session["pre_signup"]={
                "full_name": full_name,
                "email_or_phone": email_or_phone,
                "password": password
            }
            return redirect("verify")
    else:
        form = PreSignupform()
    return render(request , 'core/signup.html',{'form': form})    




def resend_otp(request):
    pre_signup = request.session.get("pre_signup")
    if not pre_signup:
        return redirect('signup')

    email_or_phone = pre_signup["email_or_phone"]
    full_name = pre_signup["full_name"]

    otp = f"{random.randint(100000, 999999)}"

    # Overwrite or create OTP
    OTPVerification.objects.update_or_create(
        email_or_phone=email_or_phone,
        defaults={"otp_code": otp}
    )

    # Send again
    if "@" in email_or_phone:
        send_mail(
            "Your OTP code (Resent)",
            f"Hello {full_name}, your new OTP is {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [email_or_phone]
        )
    else:
        sms_number = "91"+email_or_phone
        send_otp_sms(sms_number,otp)

    messages.success(request, "A new OTP has been sent.")
    return redirect("verify")


def verify_otp(request):
    pre_signup = request.session.get("pre_signup")
    if not pre_signup:
        return redirect('signup')
    email_or_phone = pre_signup["email_or_phone"]
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_input = form.cleaned_data["otp"]
            try:
                record = OTPVerification.objects.get(email_or_phone=email_or_phone)
            except OTPVerification.DoesNotExist:
                form.add_error(None,"OTP not found.")
                return render(request, "core/verify_otp.html", {"form": form})
            
            if record.is_expired():
                form.add_error(None,"OTP expired.")
            elif record.otp_code != otp_input:
                form.add_error(None, "Invalid OTP.")
            else:
                username = email_or_phone
                user = User.objects.create_user(
                    username=username,
                    password=pre_signup["password"]
                )        
                user.first_name = pre_signup["full_name"]
                user.save()

                del request.session["pre_signup"]
                record.delete()
                messages.success(request, "Account verified! You can now log in.")
                return redirect('login')
    else:
        form = OTPForm()
    return render(request,"core/verify_otp.html", {"form": form})            



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid username or Password")
    # context = {}
    return render(request,'core/login.html')


def logoutUser(request):
    logout(request)
    return redirect('home')



def home(request):
    return render(request,'core/home.html')


@login_required(login_url='login')
def hospitals(request):
    q = request.GET.get('q','')
    hospitals_qs = Hospital.objects.filter(
            Q(name__icontains=q) |
            Q(display__icontains=q) |
            Q(address__icontains=q)
        )
    # hospitals_qs = Hospital.objects.all()

    context = {"hospitals": list(hospitals_qs),"MEDIA_URL": settings.MEDIA_URL}
    return render(request, 'core/hospitals.html', context)


def bed(request):
    beds = Bed.objects.select_related('department','department_hospital').all()
    context = {'beds': beds}
    return render(request, 'core/bed.html',context)


def departments(request):
    q = request.GET.get('q','') 
    dep_qs = Department.objects.filter(
        Q(name__icontains=q)
    ).distinct()
    department_name = dep_qs.first().name if dep_qs.exists() else ''
    print( dep_qs.first())
    context = {"departments":dep_qs,
               "search_q": q,
               "department":department_name}
    return render(request,'core/opd.html',context)


def doctors(request , department_id):
    q = request.GET.get('q','')
    department = get_object_or_404(Department ,id = department_id)
    doctors = Doctor.objects.filter(
        department = department,
        name__icontains = q
        ).select_related('hospital')
    
    days_choices = Slot.DAYS_CHOICES
    select_day = request.GET.get('day')
    if select_day:
        doctors = doctors.filter(slot__days=select_day).distinct()
    context = {
        'doctors':doctors,
        'department':department,
        'days_choices':days_choices,
        'select_day':select_day
         }
    return render(request,'core/doctorlist.html',context)

@csrf_exempt
def chatbot_response(request):
    if request.method =='POST':
        data = json.loads(request.body)
        user_message = data.get("message")

        if not user_message:
            return JsonResponse({"error": "No message provided"}, status=400)

        try:
            model = gen_ai.GenerativeModel('gemini-1.5-flash-latest')
            prompt = (
                "You are a friendly AI healthcare assistant. "
                "Always greet the user with 'Hello, I am Healio your personal AI doctor. How can I help you today?'only if user say hello or hi. "
                "Your job is to suggest likely possible health conditions based on user symptoms, "
                "Do not recommend seeing a doctor unless the symptoms are very severe. "
                "Do NOT include any disclaimers. "
                "Be clear and direct in your suggestions.\n\n"
                "Just answer the user's question directly.\n\n"
                f"User: {user_message}\n"
                "Assistant:"
            )
            response = model.generate_content(prompt)
            ai_reply = response.text.strip()
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({"reply": ai_reply})

    return JsonResponse({"error": "invalid request method."}, status=405)