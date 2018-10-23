from django.contrib import admin
from .models import Profile, Projects, Ratings

# Register your models here.
admin.site.register(Projects)
admin.site.register(Profile)
admin.site.register(Ratings)