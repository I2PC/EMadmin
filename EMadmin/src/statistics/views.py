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
    print "create_all_statistics"
    acquisitions = Acquisition.objects.filter(noScipionProject=False)

    for acquisition in acquisitions:
        print "ADQUISITION", acquisitions, acquisition.noScipionProject
        # get a directory that belongs to the project
        # if it does not exits is time to close the entry
        #otherwise open a stadistic and compute it
        out_dir = os.path.join(settings.SCIPIONUSERDATA,
                               "projects", acquisition.projname, "Logs")
        if not os.path.isdir(out_dir):
            print "CLOSEEEEEEEEEEEEEEEEEE", acquisition
            acquisition.noScipionProject = True
            acquisition.save()
        else:
            print "CREATE"
            create_one_statistics(acquisition)
    return HttpResponse("Rango says hello world!")

def create_one_statistics(acquisition):
    print "create_one_statistics"
    statistics = Statistics.objects.get_or_create(acquisition=acquisition)
    script = os.path.join(settings.SCIPIONPATH,'scripts/scipionbox_report_statistics.py')
    args = ["python"]
    args += [script]
    args += ['-p', acquisition.projname]
    scipion = os.path.join(settings.SCIPIONPATH,'scipion')
    result = subprocess.Popen([scipion] +  args, stdout=subprocess.PIPE)<<<<<<<<<<<<<<<<<<<
    print json.load(result.stdout)

#    numberMovies = models.IntegerField(default=-1)
#    averageResolution = models.FloatField(default=-1)
#    resolutionData = models.TextField()
