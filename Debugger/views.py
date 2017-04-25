# coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from models import Project
from django.conf import settings
import os
from django.views import static
import WingPyUtils.http as whttp
import re
import requests


# Create your views here.
def works(request):
    return render_to_response('works.html', {'projects': list(Project.objects.all())})


def create_work(request):
    p = Project.objects.create(name=request.POST['projectName'], url=request.POST['projectUrl'])
    os.mkdir(p.get_path())
    return HttpResponseRedirect('/')


def project(request, pid):
    p = Project.objects.get(id=pid)
    dpath = p.get_path('index.html')
    if not os.path.exists(dpath):
        fpath = p.get_path('index_o.html')
        whttp.download(p.url, fpath)
        replace_site_to_local(fpath, dpath, p.get_host())
    request.session['pid'] = pid
    return static.serve(request, 'index.html', p.get_path())


def replace_site_to_local(fpath, dpath, host):
    res = None
    with open(fpath, 'r') as f:
        for i in range(2):
            f.seek(0)
            html = f.read()
            if i == 0:
                # 默认内容
                pass
            elif i == 1:
                html = html.decode('utf8')
            try:
                # 替换css、js、图片
                res = re.sub(r'(src|<link[^>]+href)="\w*?://%s/' % str(host), r'\1="/', html)
                break
            except UnicodeDecodeError:
                pass
    with open(dpath, 'w') as f:
        if res is not None and len(res) > 0:
            f.write(res)


def proxy(request):
    lpath = request.path

    if lpath.startswith('/project_'):
        # 相对路径
        lps = lpath.split('/')
        pid = lps[1].split('_')[1]
        proj = Project.objects.get(id=pid)
        proj_url = proj.url.rsplit('/', 1)[0]
        local_path = '/'.join(lps[2:])
    else:
        # 绝对路径
        try:
            pid = request.META['HTTP_REFERER'].split('/')[3].split('_')[1]
        except:
            # todo 多状态问题
            pid = request.session['pid']

        proj = Project.objects.get(id=pid)
        local_path = lpath[1:]
        proj_url = '/'.join(proj.url.split('/')[:3])

    origin_url = proj_url + '/' + local_path
    local_full_path = proj.get_path(local_path)
    local_full_path = fill_ext(local_full_path)
    if request.method == 'POST':
        return HttpResponse(requests.post(origin_url, request.POST).content)
    if not os.path.exists(local_full_path):
        whttp.download(origin_url, local_full_path, create_dirs=True)

    return static.serve(request, fill_ext(local_path), proj.get_path())


def fill_ext(path):
    ps = path.rsplit('.')
    if len(ps) >= 2:
        return path
    else:
        return path + '.html'
