# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from create_proj.models import Acquisition
import os
from django.conf import settings
from models import Statistics
import subprocess
from django.http import HttpResponse
import json

# Create your views here.

@login_required
def create_all_statistics(request):
    acquisitions = Acquisition.objects.filter(noScipionProject=False)

    for acquisition in acquisitions:
        # get a directory that belongs to the project
        # if it does not exits is time to close the entry
        #otherwise open a stadistic and compute it
        out_dir = os.path.join(settings.SCIPIONUSERDATA,
                               "projects", acquisition.projname, "Logs")
        create_one_statistics(acquisition)
    return HttpResponse("Rango says hello world!")

def create_one_statistics(acquisition):
    out_dir = os.path.join(settings.SCIPIONUSERDATA,
                           "projects", acquisition.projname, "Logs")
    if acquisition.noScipionProject == True:
        return None
    elif not os.path.isdir(out_dir):
        acquisition.noScipionProject = True
        acquisition.save()
        return None

    statistic = Statistics.objects.get_or_create(acquisition=acquisition)[0]
    script = os.path.join(settings.SCIPIONPATH,'scripts/scipionbox_report_statistics.py')
    args = ["python"]
    args += [script]
    args += ['-p', acquisition.projname]
    scipion = os.path.join(settings.SCIPIONPATH,'scipion')

    p = subprocess.Popen([scipion] +  args, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode
    d = json.loads(err)
    if d:
        statistic.averageResolution =  d['averageResolution']
        statistic.resolutionData = json.dumps(d['resolutionData'])
        statistic.numberMovies = d['numberMovies']
        statistic.save()
    return statistic