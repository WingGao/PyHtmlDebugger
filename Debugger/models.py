from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import os


# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)

    def get_path(self, fname=''):
        return os.path.join(settings.WORK_DIR, str(self.id), fname)

    def get_host(self):
        res = self.url.split('://')[-1]
        return res.split('/', 1)[0]

