from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from models import Project
from django.conf import settings
import os


# Create your views here.
def works(request):
    return render_to_response('works.html', {'projects': list(Project.objects.all())})


def create_work(request):
    p = Project.objects.create(name=request.POST['projectName'].strip())
    os.mkdir(p.get_path())
    return HttpResponseRedirect('/')


def project(request, pid):
    return HttpResponse(pid)


def proxy(request):
    return HttpResponse(1)
