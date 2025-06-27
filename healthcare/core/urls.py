from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home , name='home'),
    path('hospitals/', views.hospitals, name='hospitals'),
    path('departments/',views.departments,name='departments'),
    path('doctors/<int:department_id>/',views.doctors,name='doctors')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)