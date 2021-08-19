from django.db import models


# Create your models here.
class Urls(models.Model):
    original_url = models.CharField(max_length=255, blank=False)
    hash_url = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.original_url
