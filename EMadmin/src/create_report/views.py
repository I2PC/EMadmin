# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_tables2 import RequestConfig
from django.http import HttpResponse

from django.shortcuts import render, reverse
from create_proj.models import Acquisition
from create_report.tables import ProjectsTable
from django.conf import settings
from django.contrib.auth.decorators import login_required
import jinja2
#from jinja2 import Template
import os
from create_stat.views import create_one_statistics
from create_stat.models import  Statistics
from create_report.plot import doPlot
import json
import numpy as np
import unidecode

@login_required
def create_report(request):
#    return render(request, 'create_report/report.html', {'report': Acquisition.objects.all()})
    user = request.user
    if user.is_staff:
        queryset =  Acquisition.objects.filter(acquisition2__isnull=False).order_by('-date')
    else:
        queryset = Acquisition.objects.filter(user=user, acquisition2__isnull=False).order_by('-date')

    table = ProjectsTable(queryset)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render(request, 'create_report/report.html', {'report': table})

import re

def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless ',
        '>': r'\textgreater ',
    }
    regex = re.compile('|'.join(re.escape(unicode(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)

@login_required
def create_report_latex(request, idacquisition):
    # init template procesor jinja2 for
    latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('/'))
    )
    acquisition = Acquisition.objects.get(pk=idacquisition)
    # fill statistics entry
    statistic = create_one_statistics(acquisition)
    if statistic:
        numberMicrographs = statistic.numberMovies
    else:
        try:
            statistic = Statistics.objects.get(acquisition=acquisition)
            numberMicrographs = statistic.numberMovies
        except Statistics.DoesNotExist:
            numberMicrographs = -1

    latexTemplateFile = settings.LATEX_REPORT_TEMPLATE
    latexLogoFile = settings.LATEX_REPORT_TEMPLATE_ICON
    template = latex_jinja_env.get_template(os.path.realpath(latexTemplateFile))

    options = {}
    # Header
    options['acquisitionDate'] = acquisition.date.strftime('%Y-%m-%d %H:%M')
    options['acquisitionUserName'] = tex_escape(acquisition.user.name)
    options['acquisitionId'] = acquisition.id
    options['acquisitionProjName'] = tex_escape(acquisition.projname)
    options['acquisitionSample'] = tex_escape(acquisition.sample)
    options['acquisitionBackupPath'] = tex_escape(acquisition.backupPath)
    options['acquisitionShiftLength'] = acquisition.shiftLength

    # Microscope
    options['microscopeName'] = tex_escape(acquisition.microscope.name)
    options['microscopeModel'] = tex_escape(acquisition.microscope.model)
    options['microscopeDetector'] = tex_escape(acquisition.microscope.detector)
    options['acquisitiondetectorPixelSize'] = acquisition.microscope.detectorPixelSize
    options['microscopeCs'] = acquisition.microscope.cs

    acquisition2 = acquisition.acquisition2
    # Acquisition Params
    options['acquisitionWorkflow'] = tex_escape(acquisition.workflow.name)
    options['acquisitionVoltage'] = acquisition.voltage
    options['acquisitionNominalMagnification'] = acquisition2.nominal_magnification
    options['acquisitionSamplingRate'] = acquisition2.sampling_rate
    options['acquisitionSpotSize'] = acquisition2.spotsize
    options['aquisitionIlluminatedArea'] = acquisition2.illuminated_area

    # Dose & Fractions
    options['acquisitionDosePerFraction'] = acquisition2.dose_per_fraction
    options['acquisitionTotalExptime'] = acquisition2.total_exposure_time
    options['acquisitionNumFrames'] = acquisition2.number_of_fractions
    options['acquisitionFramesPerFrac'] = acquisition2.frames_in_fraction

    # EPU parameters  acquisitionDefocusDistance
    options['acquisitionNominalDefocusRange'] = acquisition2.nominal_defocus_range
    options['acquisitionAutoDefocusDistance'] = acquisition2.autofocus_distance
    options['acquisitionDriftMeassurement'] = acquisition2.drift_meassurement
    options['acquisitionDelayAfterStageShift'] = acquisition2.delay_after_stage_shift
    options['acquisitionDelayAfterImageShift'] = acquisition2.delay_after_image_shift
    options['acquisitionMaxImageShift'] = acquisition2.max_image_shift
    options['acquisitionExposureHole'] = acquisition2.exposure_hole

    # Apertures
    options['acquisitionC2'] = acquisition2.c2
    options['acquisitionO1'] = acquisition2.o1
    options['acquisitionPhP'] = acquisition2.php

    #logo
    options['mic_jpg'] = latexLogoFile

    #processing
    options['acquisitionWorkflowName'] = tex_escape(acquisition.workflow.name)
    options['statisticsNumberMovies'] = numberMicrographs
    options['pgfResolutionFile'] = ""


    # if project exists compile data in scipionuserdata/project/Logs
    # otherwise use /tmp
    out_dir=os.path.join(settings.SCIPIONUSERDATA, "projects", acquisition.projname, "Tmp")
    if os.path.isdir(out_dir):
        pass
    else:
        out_dir = "/tmp"
    out_file_root=os.path.join(out_dir,"temp")

    # create histograms and plot them
    if numberMicrographs > 0:
        pgfResolution, pdfResolution = doPlot(np.array(json.loads(statistic.resolutionData)),
               "resolution (A)",
               "no Movies",
               out_file_root+"staRes")
        options['pgfResolutionFile'] = pgfResolution
        pgfDefocus, pdfDefocus = doPlot(np.array(json.loads(statistic.defocusData)),
               "defocus (A)",
               "no Movies",
               out_file_root+"staDef")
        options['pgfDefocusFile'] = pgfDefocus
        print("RES DEF", pgfResolution, pgfDefocus)
        options['dataavailable'] = '\longtrue'
    else:
        print("No micrographs to process")
        options['dataavailable'] = '\longfalse'
    renderer_template = template.render(**options)
    with open(out_file_root + ".tex", "w") as f:  # saves tex_code to outpout file
        f.write(unidecode.unidecode(renderer_template)) 

    os.system('pdflatex -output-directory %s %s'%(out_dir, out_file_root))
    with open(os.path.join(out_dir, out_file_root + ".pdf"), 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.close()
    return HttpResponse("Ca not create report")
