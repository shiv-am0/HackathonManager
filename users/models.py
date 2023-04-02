from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    registered_hackathon = models.CharField(max_length=100, default='.')
    is_super_user = models.BooleanField(default='false')

    def __str__(self):
        return self.user.username


class Hackathon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    submission_name = models.CharField(max_length=100)
    summary = models.CharField(max_length=200)
    hackathon_title = models.CharField(max_length=100)
    github_link = models.CharField(max_length=200)
