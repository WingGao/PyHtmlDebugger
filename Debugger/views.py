# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from models import Project
from django.conf import settings
import os
from django.views import static
import WingPyUtils.http as whttp


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
        whttp.download(p.url, p.get_path('index.html'))
    return static.serve(request, 'index.html', p.get_path())


def proxy(request):
    pid = request.META['HTTP_REFERER'].split('/')[-1]
    proj = Project.objects.get(id=pid)
    lpath = request.path

    if lpath.startswith('/project/'):
        # 相对路径
        proj_url = proj.url.rsplit('/', 1)[0]
        local_path = lpath[9:]

    else:
        # 绝对路径
        local_path = lpath[1:]
        proj_url = '/'.join(proj.url.split('/')[:3])

    orgin_url = proj_url + '/' + local_path
    local_full_path = proj.get_path(local_path)

    if not os.path.exists(local_full_path):
        whttp.download(orgin_url, local_full_path, create_dirs=True)

    return static.serve(request, local_path, proj.get_path())
