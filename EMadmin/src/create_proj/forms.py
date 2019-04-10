from django import forms
from create_proj.models import Acquisition, Acquisition2
#from create_proj.fields import ListTextWidget
import os
from django.conf import settings
import subprocess
#import re
from create_proj.models import Acquisition
from datetime import datetime, timedelta

#kill port sudo lsof -t -i tcp:8000 | xargs kill -9
class SkipAcquisitionForm(forms.Form):
    def __init__(self, *args, **kwargs):
         """Get projects done last week by current user"""
         user = kwargs.pop('user',None)
         last_week = datetime.today() - timedelta(days=7)
         super(SkipAcquisitionForm, self).__init__(*args, **kwargs)
         if user.is_staff:
             self.fields['project'].queryset =  \
                 Acquisition.objects.filter(
                     date__gte=last_week).order_by('-date')
         else:
             self.fields['project'].queryset =  \
                 Acquisition.objects.filter(
                     date__gte=last_week, user=user).order_by('-date')

    """Show objects recorded last week"""
    project = forms.ModelChoiceField(queryset=None, initial=0)

class AcquisitionForm(forms.ModelForm):
    shiftLength = forms.FloatField(initial=3, label="Turn length (days)")
    backupPath = forms.CharField(required=False,
                                 label="Backup (double click to see disks)",
                                 widget=forms.HiddenInput())
    schedule = forms.BooleanField(widget= forms.CheckboxInput(),initial=False,
                                  label="Run scipion in batch mode (schedule)",
                                  required=False)
    multiple_backup = forms.BooleanField(initial=False,
                                  label="Ignore backup warning",
                                  required=False,
                                  widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        try:
            if os.path.isdir(settings.BACKUPPATH):
                _dir_list = [os.path.join(settings.BACKUPPATH, o)
                         for o in os.listdir(settings.BACKUPPATH)
                         if os.path.isdir(os.path.join(settings.BACKUPPATH,o))]
            else:
                 data_list = []
            super(AcquisitionForm, self).__init__(*args, **kwargs)
#            self.fields['backupPath'].widget = ListTextWidget(
#                    data_list=_dir_list, name='dir-list', size=40)
        except:
            data_list = []  # directory does not exists

#    def clean_backupPath(self):
    def clean(self):
        def is_running(process):
            from subprocess import check_output
            try:
                pidList = check_output(["pidof",process])
            except subprocess.CalledProcessError:
                pidList = [0]
            return pidList

        # if  lsyncd running report error TRANSFERTOOL
        counterList = is_running(settings.TRANSFERTOOL)
        # print "lsync pid =", counterList
        # for k, v in self.cleaned_data.iteritems():
        #     print "**", k, v, "**"
        if counterList[0] != 0 and\
                (not self.cleaned_data.get('multiple_backup')):
            msg = "There is at least one backup script running in the " \
                  "background " \
                  "Consider killing it. Execute in a terminal: " \
                  "'ps -ef | grep %s' to get a list with the  processes." \
                  "Use 'kill -9 process_number' to kill the process. " \
                  "If you want to ignore this warning select 'ignore " \
                  "backup warning' and resend the " \
                  "form" % settings.TRANSFERTOOL
            raise forms.ValidationError(msg)
        return self.cleaned_data

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Acquisition
#        fields = ('microscope','workflow', 'voltage',
#                  'sample', 'date','backupPath')
        exclude = ('user', 'projname', 'date', 'noScipionProject')

class AcquisitionForm2(forms.ModelForm):
    # An inline class to provide additional information on the form.
    sampling_rate =\
        forms.FloatField(label="Sampling rate (A/px^2)",
                         help_text="Movie pixel rate in Angstroms per pixel")
    dose_rate =\
        forms.FloatField(label="Dose rate (e/(px^2*sec)) ",
                         help_text = "Dose rate in electrons per pixels"
                                     " and per second",
                         initial=0)
    total_exposure_time =\
        forms.FloatField(label="Total exposure time per movie (sec)",
                         help_text='If you fill this field Total Dose per '
                                   'Movie will be automatically filled in',
                         initial=0)
    total_dose_per_movie =\
        forms.FloatField(label="Total dose per movie(e/A^2)",
                         help_text='If you fill this field Total Exposure '
                                   'Time per Movie will be automatically '
                                   'filled in',
                         initial=0)
    illuminated_area =\
        forms.FloatField(label="Illuminated area (microns)",
                         help_text = 'Electron Beam Diameter at the specimen'
                                     ' surface, defined by the settings of the'
                                     ' Condenser lenses (mainly C1).'
                                     ' Units: microns')

    autofocus_distance = forms.FloatField(label='Autofocus periodicity',
                                          help_text = '0 -> always')

    field_order = ['sampling_rate', 'dose_rate', 'total_exposure_time',
                   'total_dose_per_movie', 'dose_last_fraction',
                   'number_of_fractions',  'frames_in_fraction',
                   'nominal_magnification', 'spotsize',
                   'illuminated_area', 'nominal_defocus_range'
                   ]

    def __init__(self, *args, **kwargs):
        super(AcquisitionForm2, self).__init__(*args, **kwargs)
        self.fields['dose_in_last_fraction'].help_text = \
            'Set to -1 if the rate is equal to the other fractions.' \
            'Units e/A^2 (TODO: CHECK UNIST)'
        self.fields['frames_in_fraction'].help_text = \
            'Fractions are an average of a few frames computed by ' \
            'the microscope software'
        self.fields['number_of_fractions'].help_text = \
            'Number of images in a movie'
        self.fields['nominal_magnification'].help_text = \
            'Ratio between the length of a test object and the length of the ' \
            'same object in the detector.'
        self.fields['spotsize'].help_text =\
            'Value of spotsize knot -Electron Beam Diameter after C1 lens-'
        self.fields['nominal_defocus_range'].help_text = \
            'Minimum, maximun and step in defocus range.'
        self.fields['c2'].help_text = 'condenser lens'
        self.fields['o1'].help_text = 'objective aperture'
        self.fields['php'].help_text = 'which phase plate are we using'
        self.fields['php_position_start'].help_text = \
            'phase plate starting position'
        self.fields['php_periodicity'].help_text = \
            'number movies taken at each phase plate position'

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Acquisition2
        #labels = {
        #    "video": "Embed"
        #}
        #fields = ('pixelsize','dose')
        exclude = ('acquisition', 'dose_per_fraction')
