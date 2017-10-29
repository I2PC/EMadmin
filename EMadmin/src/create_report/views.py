# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_tables2 import RequestConfig

from django.shortcuts import render, reverse
from create_proj.models import Acquisition
from tables import ProjectsTable
from django.conf import settings

# Create your views here.
#AUX FUNCTION FOR CREATE REPORT
def create_report(request):
#    return render(request, 'create_report/report.html', {'report': Acquisition.objects.all()})

    table = ProjectsTable(Acquisition.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'create_report/report.html', {'report': table})

def create_report_latex(request, idacquisition):
    acquisition = Acquisition.objects.get(pk=idacquisition)

    print "project_name", idacquisition, settings.LATEX_REPORT_TEMPLATE
