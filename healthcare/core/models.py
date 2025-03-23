from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True,null=True)
    dispaly = models.FileField(blank=True, null=True)
     

class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('EMERGENCY','Emergency'),
        ('CHEST','Chest'),
        ('HEART','Heart'),
        ('ORTHO','Orthopedic'),
    ]
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,choices=DEPARTMENT_CHOICES)


class Doctor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    opd_duration = models.PositiveBigIntegerField()


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
        return self.name


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
    slot = models.DateTimeField()


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
    units_available = models.PositiveBigIntegerField(default=0)