from django.contrib import admin
from. models import Hospital,Department,Doctor,Patient,Bed,Slot,Appointment,Bloodbank

# Register your models here.

admin.site.register(Hospital)
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Bed)
admin.site.register(Slot)
admin.site.register(Appointment)
admin.site.register(Bloodbank)