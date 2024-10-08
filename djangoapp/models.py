from django.db import models
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt
# Create your models here.




class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField()
    city = models.CharField(max_length=100)
    marks = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
    
class Problems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    
    
    
class OtpCode(models.Model):
    otpcode = models.CharField(max_length=6)
    email = models.CharField(max_length=50)
    def __str__(self):
        return self.otpcode
    
    
    
    
    
class StudyMaterials(models.Model):
    title = models.CharField(max_length=100)
    pptx = models.FileField(upload_to='pptx/')
    password = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    
class VisitCount(models.Model):
    count = models.IntegerField(default=0)
    
    


class ShareProblems(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    code = encrypt(models.TextField(max_length=255))
    tags = encrypt(models.CharField(max_length=255))
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    
    
class Degree(models.Model):
    servo_name = models.CharField(max_length=100, default='servo')
    degree1 = models.CharField(max_length=100, default=0)
    degree2 = models.CharField(max_length=100, default=0)
    degree3 = models.CharField(max_length=100, default=0)
    def __str__(self):
        return self.servo_name