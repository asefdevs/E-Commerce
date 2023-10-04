from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(
        max_length=64, blank=True, null=True)

    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user_profile')
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,blank=True,null=True)
    birthdate=models.DateField(blank=True, null=True)
    height=models.PositiveIntegerField(blank=True,null=True)
    phone_number=models.CharField(max_length=255,blank=True,null=True)
    
    profile_photo=models.ImageField(blank=True,null=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if  self.profile_photo:
            img=Image.open(self.profile_photo.path)
            if img.height>600 or img.width>600:
                output_size=(600,600)
                img.thumbnail(output_size)
                img.save(self.profile_photo.path)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'



