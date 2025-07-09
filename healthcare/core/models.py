from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.
User = get_user_model()

class OTPVerification(models.Model):
    email_or_phone = models.CharField(max_length=100,unique=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=5)


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True,null=True)
    display = models.FileField(upload_to='media/hospital_images/', blank=True, null=True)
     
    general_beds = models.PositiveIntegerField(default=0)
    cabin_beds = models.PositiveIntegerField(default=0)
    icu_beds = models.PositiveIntegerField(default=0)
    ventilator_beds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
     

class Department(models.Model):
    DEPARTMENT_CHOICES = [
    ('ENT', 'ENT'),
    ('CARDIOLOGY', 'Cardiology'),
    ('ORTHO', 'Orthopedics'),
    ('PEDIATRICS', 'Pediatrics'),
    ('GASTROENTEROLOGY', 'Gastroenterology'),
    ('NEUROLOGY', 'Neurology'),
    ('GYNECOLOGY', 'Gynecology & Obstetrics'),
    ('DERMATOLOGY', 'Dermatology'),
    ('ONCOLOGY', 'Oncology'),
    ('NEPHROLOGY', 'Nephrology'),
    ('PULMONOLOGY', 'Pulmonology'),
    ('OPHTHALMOLOGY', 'Ophthalmology'),
]

    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name  = models.CharField(max_length=100, default="Unnamed Doctor")
    qualification = models.CharField(max_length=100,default="unknonwed")
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE ,default=1)
    opd_duration = models.PositiveBigIntegerField()

    def get_opd_timing_display(self):
       slots = self.slot_set.all()
       if not slots:
         return "No slots available"
       return ", ".join([f"{slot.days} ({slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')})" for slot in slots])
    
    def __str__(self):
        return self.name



class Patient(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class Bed(models.Model):
    CATEGORY_CHOICES = [
        ('GOV', 'Government'),
        ('PRI', 'Private'),
        ('PUB', 'Public'),
    ]
    BED_TYPE_CHOICES = [
        ("GENERAL_BED", "General Bed"),
        ("ICU_BED", "Icu Bed"),
        ("CABIN_BED", "Cabin Bed"),
        ("VENTILATOR_BED", "Ventilator Bed"),
    ]
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    bed_type = models.CharField(choices=BED_TYPE_CHOICES,max_length=20)
    allocated_to = models.ForeignKey(Patient,on_delete=models.CASCADE,blank=True,null=True)
    under = models.ForeignKey(Doctor,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.bed_type + " - " + self.department.name


class Slot(models.Model):
    DAYS_CHOICES = [
        ('MONDAY','Monday'),
        ('TUESDAY','Tuesday'),
        ('WEDNESDAY','Wednesday'),
        ('THURSDAY','Thursday'),
        ('FRIDAY','Friday'),
        ('SATURDAY','Saturday'),
        ('SUNDAY','Sunday'),
    ]
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    days = models.CharField(max_length=10,choices=DAYS_CHOICES,blank=True,null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Appointment(models.Model):
    patient =  models.ForeignKey(Patient,on_delete=models.CASCADE,blank=True,null=True)
    doctor =  models.ForeignKey(Doctor,on_delete=models.CASCADE,blank=True,null=True)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(blank=True, null=True) 



class Bloodbank(models.Model):
    BLOOD_GRP_CHOICES = [
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('O+','O+'),
        ('O-','O-'),
        ('AB+','AB+'),
        ('AB-','AB-')
    ]
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    bld_grps = models.CharField(max_length=5, choices=BLOOD_GRP_CHOICES)
    units_available = models.PositiveIntegerField(default=0)