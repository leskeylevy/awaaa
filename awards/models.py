from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.core.validators import MaxValueValidator, MinValueValidator
import numpy as np


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
    def search_by_name(cls, search_term):
        proje = cls.objects.filter(name__icontains=search_term)
        return proje

    def average_rating(self):
        all_ratings = list(map(lambda x: x.design, self.ratings.all()))
        # all_ratings = list(map(lambda x: x.content, self.ratings_set.all()))
        # all_ratings = list(map(lambda x: x.usability, self.ratings_set.all()))
        # all_ratings = list(map(lambda x: x.usability, self.ratings_set.all()))
        return np.mean(all_ratings)


class Ratings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='ratings')
    design = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    usability = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    creativity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    content = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    @classmethod
    def get_all(cls):
        all_objects = Review.objects.all()
        return all_objects



class Comments(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Projects, related_name='comments')
    comment = models.CharField(max_length=150)
