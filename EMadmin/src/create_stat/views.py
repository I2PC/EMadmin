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
from fusioncharts import FusionCharts
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
    return HttpResponse("Hi from create_all_statistics")

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
    if not os.path.exists(script):
        print "HORROR script %d does not exist" % script
        exit(-1)
    args = ["python"]
    args += [script]
    args += ['-p', acquisition.projname]
    scipion = os.path.join(settings.SCIPIONPATH,'scipion')

    p = subprocess.Popen([scipion] +  args, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, err = p.communicate()
    # if err contains something else (in addition to the dict)
    # remove it
    err = err[err.find("{"):err.find("}")+1]
    rc = p.returncode
    d = json.loads(err)
    if d:
        statistic.averageResolution =  d['averageResolution']
        statistic.resolutionData = json.dumps(d['resolutionData'])
        statistic.defocusData = json.dumps(d['defocusData'])
        statistic.numberMovies = d['numberMovies']
        statistic.save()
    return statistic

from datetime import datetime, timedelta
@login_required
def create_resolution_plot(request):
    statistics = Statistics.objects.all()
    category=""
    data=""
    for statistic in statistics:
        if statistic.numberMovies > 25:
            data += str(statistic.averageResolution) + "|"
            category += str(statistic.acquisition.date.strftime('%Y-%m-%d')) + "|"
    _zoomline = FusionCharts("zoomline", "ex1" , "800", "550", "chart-1",
                             "json",
    # The chart data is passed as a string to the `dataSource` parameter.
    """{
    "chart": {
        "caption": "Resolution vs Time",
        "subcaption": "Last year",
        "yaxisname": "Unique Visitors",
        "xaxisname": "Date",
        "yaxisminValue": "0",
        "yaxismaxValue": "14",
        "pixelsPerPoint": "0",
        "pixelsPerLabel": "30",
        "lineThickness": "1",
        "compactdatamode": "1",
        "dataseparator": "|",
        "labelHeight": "30",
        "theme": "fint"
    },
    "categories": [
        {
            "category": "%s"
        }
    ],
    "dataset": [
        {
            "seriesname": "talos",
            "data": "%s"
        }    ]
}"""%(category, data))

    return  render(request, 'create_stat/chart.html', {'output' :
                                                      _zoomline.render()})