from django.test import TestCase
import views
import models
from django.conf import settings
import os


# Create your tests here.
class DebuggerTest(TestCase):
    def setUp(self):
        self.proj = models.Project(url='http://wow.techbrood.com/static/20151209/14902.html')

    def testReplace(self):
        views.replace_site_to_local(os.path.join(settings.WORK_DIR, '3', 'index.html'), self.proj.get_host())
