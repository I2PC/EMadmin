# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_tables2 import RequestConfig
from django.http import HttpResponse

from django.shortcuts import render, reverse
from create_proj.models import Acquisition
from tables import ProjectsTable
from django.conf import settings
from django.contrib.auth.decorators import login_required
import jinja2
#from jinja2 import Template
import os


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
    latexTemplateFile = settings.LATEX_REPORT_TEMPLATE
    latexLogoFile = settings.LATEX_REPORT_TEMPLATE_ICON
    template = latex_jinja_env.get_template(os.path.realpath(latexTemplateFile))

    options = {}
    # Header
    options['acquisitionDate'] = acquisition.date.strftime('%Y-%m-%d %H:%M')
    options['acquisitionUserName'] = acquisition.user.name
    options['acquisitionId'] = acquisition.id
    options['acquisitionProjName'] = acquisition.projname
    options['acquisitionSample'] = acquisition.sample
    options['acquisitionBackupPath'] = acquisition.backupPath
    options['acquisitionShiftLength'] = acquisition.shiftLength

    # Microscope
    options['microscopeName'] = acquisition.microscope.name
    options['microscopeModel'] = acquisition.microscope.model
    options['microscopeDetector'] = acquisition.microscope.detector
    options['acquisitiondetectorPixelSize'] = acquisition.microscope.detectorPixelSize
    options['microscopeCs'] = acquisition.microscope.cs

    acquisition2 = acquisition.acquisition2
    # Acquisition Params
    options['acquisitionWorkflow'] = acquisition.workflow.name
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
    options['acquisitionWorkflowName'] = acquisition.workflow

    # if project exists compile data in scipionuserdata/project/Logs
    # otherwise use /tmp
    out_dir=os.path.join(settings.SCIPIONUSERDATA, "projects", acquisition.projname, "Logs")
    if os.path.isdir(out_dir):
        pass
    else:
        out_dir = "/tmp"
    out_file=os.path.join(out_dir,"temp.tex")
    renderer_template = template.render(**options)
    with open(out_file, "w") as f:  # saves tex_code to outpout file
        f.write(renderer_template.replace("_","\_")) #protec again wiard characters

    os.system('pdflatex -output-directory %s %s'%(out_dir, out_file)),
    with open(os.path.join(out_dir,out_file.replace(".tex",".pdf")), 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.close()
    return HttpResponse("Ca not create report")
