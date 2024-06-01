from django.db import models

# Create your models here.


class Registration(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to ="media/user/%y")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username