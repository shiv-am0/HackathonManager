from django.contrib import admin
from .models import Profile, Hackathon, Submission

# Register your models here.
admin.site.register(Profile)
admin.site.register(Hackathon)
admin.site.register(Submission)
