from django.db import models
from django.contrib.auth.models import User

#Create your models here
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    # password = models.CharField(max_length=128, unique=True)
    college_id = models.CharField(max_length=10, unique=True)
    subject = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='faculty_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    

class Faculty_Attendence(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attendence = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Present' if self.attendence else 'Absent'}"