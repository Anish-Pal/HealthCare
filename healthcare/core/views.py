from django.shortcuts import render
from . models import Hospital

# Create your views here.

def home(request):
    return render(request,'core/home.html')


def hospitals(request):
    q = request.GET.get('q')  if request.GET.get('q') != None else ''
    hospitals_qs = Hospital.objects.filter(name__icontains=q).values_list("name", "display")
    return render(request, 'core/hospitals.html', context={"hospitals": list(hospitals_qs)})
