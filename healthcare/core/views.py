from django.shortcuts import render , get_object_or_404
from django.conf import settings
from django.db.models import Q
from . models import Hospital
from . models import Bed
from . models import Department
from . models import Doctor , Slot

# Create your views here.

def home(request):
    return render(request,'core/home.html')


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