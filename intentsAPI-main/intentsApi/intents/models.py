from django.db import models

# Create your models here.
class Intents(models.Model):
    tag = models.CharField(max_length=30, unique=True)
    patterns=models.JSONField()
    responses=models.JSONField()
class Unidentified(models.Model):
    messages = models.TextField()