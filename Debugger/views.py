# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from models import Project
from django.conf import settings
import os
from django.views import static
import urllib


# Create your views here.
def works(request):
    return render_to_response('works.html', {'projects': list(Project.objects.all())})


def create_work(request):
    p = Project.objects.create(name=request.POST['projectName'], url=request.POST['projectUrl'])
    os.mkdir(p.get_path())
    return HttpResponseRedirect('/')


def project(request, pid):
    p = Project.objects.get(id=pid)
    if not os.path.exists(p.get_path('index.html')):
        download(p.url, p.get_path('index.html'))
    return static.serve(request, 'index.html', p.get_path())


def proxy(request):
    pid = request.META['HTTP_REFERER'].split('/')[-1]
    proj = Project.objects.get(id=pid)
    lpath = request.path
    if lpath.startswith('/project/'):
        # 相对路径
        local_path = lpath[9:]
        orgin_url = proj.url + local_path
        local_full_path = proj.get_path(local_path)

    if not os.path.exists(local_full_path):
        dirname = os.path.dirname(local_full_path)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        download(orgin_url, local_full_path)

    return static.serve(request, local_path, proj.get_path())


def download(url, name):
    urllib.urlretrieve(url, name)
