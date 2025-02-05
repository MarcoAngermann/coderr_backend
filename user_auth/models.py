from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(unique=True, error_messages={'unique': "Email bereits vorhanden."})
    username = models.CharField(max_length=150, default='your_name')
    type = models.CharField(max_length=100, choices=[('business', 'business'), ('customer', 'customer')])
    created_at = models.DateTimeField(auto_now_add=True, blank=True) 
    first_name = models.CharField(max_length=100, default = 'Your')
    last_name = models.CharField(max_length=100, default='Name')
    file = models.FileField(blank=True, null=True, upload_to='uploads/')
    location = models.CharField(max_length=100, default = 'location')
    description = models.TextField(max_length=1000, default = '')
    working_hours = models.CharField(max_length=100, default = '8 - 16')
    tel = models.CharField(max_length=100, default = '1234567890')
    uploaded_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """
        Saves the current instance. Overwrites the username with the username of the associated User.
        Updates the uploaded_at field if the file has changed.
        """
        self.username = self.user.username
        if self.pk:  
            original = Profile.objects.get(pk=self.pk)
            if original.file != self.file:  
                self.uploaded_at = now()
        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.user.username} - {self.type}"





