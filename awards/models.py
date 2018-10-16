from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import datetime as dt


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dp = models.ImageField(upload_to='images')
    bio = HTMLField(max_length=500)
    contact = models.CharField(max_length=100)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def __str__(self):
        return self.user.username


class Projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')
    video = models.FileField(upload_to='videos', null=True)
    postedon = models.DateTimeField(auto_now_add=True)
    link = models.URLField()

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['postedon']

    @classmethod
    def get_all(cls):
        projects = cls.objects.order_by('postedon')
        return projects

    @classmethod
    def search_by_name(cls,search_term):
        proje = cls.objects.filter(name__icontains=search_term)
        return proje



