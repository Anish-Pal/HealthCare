from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from . models import Hospital

# Create your views here.

def home(request):
    return render(request,'core/home.html')


def hospitals(request):
    q = request.GET.get('q')  if request.GET.get('q') != None else ''
    hospitals_qs = Hospital.objects.filter(
    Q(name__icontains=q) |
    Q(display__icontains=q) | 
    Q(address__icontains=q)
    ).values("name", "display","address")
    context = {"hospitals": list(hospitals_qs),"MEDIA_URL": settings.MEDIA_URL }
    return render(request, 'core/hospitals.html', context)



