# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.db import models
from django.utils.text import slugify
from django.conf import settings

# workflow
class Workflow(models.Model):
    name = models.CharField(max_length=128, blank=False)
    workflow = models.TextField(unique=True, blank=False)
    date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name

# Create your models here.
class Microscope(models.Model):
    name      = models.CharField(max_length=64, unique=True, blank=False)
    model     = models.CharField(max_length=128, unique=True, blank=False)
    detector  = models.CharField(max_length=64, unique=True, default='FalconIII')
    detectorPixelSize = models.FloatField(default=14)  # microns
    cs = models.FloatField(default=2.7)  #           mm
    # microscope data is in this folder
    dataFolder = models.CharField(max_length=256,
                                  default='/home/scipionuser/OffloadData')

    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name

class Acquisition(models.Model):
    microscope = models.ForeignKey(Microscope, default=settings.DEFAULTMIC,
                                   on_delete=models.CASCADE)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,
                                   on_delete=models.CASCADE)
    workflow   = models.ForeignKey(Workflow, default=settings.DEFAULTWORKFLOWID,
                                   on_delete=models.CASCADE)
    sample     = models.CharField(max_length=128)
    voltage    = models.IntegerField(default=200)
    date       = models.DateTimeField(default=timezone.now, blank=True)  #
    shiftLength = models.FloatField(default=3)
    projname   = models.CharField(max_length=128, blank=True, unique=True)  #
    backupPath = models.CharField(max_length=128,
                                  default='NOBACKUP',blank=True)
    multiple_backup = models.BooleanField(default=False)
    schedule = models.BooleanField(default=False)
    noScipionProject = models.BooleanField(default=False)  # scipion project
                                                         # no available

    def save(self, *args, **kwargs):
        #create project name
        user_name = slugify(self.user.name)
        sample_name = slugify(self.sample)
        self.projname = "%s_%s_%s"%(self.date.strftime('%Y_%m_%d'),
                                    user_name, sample_name)
        super(Acquisition, self).save(*args, **kwargs)

    def __str__(self):  #For Python 2, use __str__ on Python 3
        try:
            return "user=%s, sample=%s, date=%s"%(self.user,
                                                  self.sample,
                                                  self.date.strftime('%Y-%m-%d '
                                                                   '%H:%M'))
        except:
            return "sample=%s, date=%s"%(self.sample,
                                         self.date.strftime('%Y-%m-%d '
                                                                   '%H:%M'))


DRIFT_MEASU_CHOICES = [('never', 'never'), ('always', 'always'),('gridsquare','gridsquare')]
EXPOSURE_HOLE_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4,'4'), (5,'5')]
C2_CHOICES = [(30, '30'), (50, '50'),(70, '70'),(150, '150')]
O1_HOLE_CHOICES = [(0, '--'), (70, '70'), (100, '100')]
PHP_CHOICES = [(0, '--'), (1, '1'), (2, '2'),(3, '3'), (4, '4'), (5, '5'), (6, '6')]

class Acquisition2(models.Model):
    acquisition = models.OneToOneField(Acquisition, on_delete=models.CASCADE)
    nominal_magnification = models.FloatField(blank=False)
    sampling_rate = models.FloatField(blank=False)  # A/px OK
    spotsize = models.FloatField(blank=False)
    illuminated_area = models.FloatField(blank=True, default=1.68) #microns OK

    # DOSE IN FRACTION NOT FOR FORM
    dose_per_fraction = models.FloatField(blank=False, default=0)
    dose_in_last_fraction = models.FloatField(blank=False, default=-1, null=True)
    # e/A^2 y fraction--> change frame by fraction, OK
    dose_rate = models.FloatField(blank=False)  # e/px*sec
    total_exposure_time = models.FloatField(blank=False) # seconds
    number_of_fractions = models.PositiveIntegerField(blank=False)
    frames_in_fraction = models.PositiveIntegerField(blank=False)
    total_dose_per_movie = models.FloatField(blank=False, default=-1, null=True)
    nominal_defocus_range = \
        models.CharField(
            max_length=128, blank=False, default="min, max, step")  # array the floats microns
    autofocus_distance = models.FloatField(blank=False)

    #
    drift_meassurement = models.CharField(max_length=16,
                                          choices=DRIFT_MEASU_CHOICES,
                                          default='never')
    # wait this seconds before taken a new movie
    delay_after_stage_shift = models.IntegerField(default=5)
    delay_after_image_shift = models.IntegerField(default=5)

    # max defocus distance (unit microns)
    max_image_shift = models.IntegerField(default=5)

    exposure_hole = models.IntegerField(choices=EXPOSURE_HOLE_CHOICES,
                                      default=1)
    # condenser lens
    c2 = models.IntegerField(choices=C2_CHOICES,
                                      default=50)
    # objective aperture
    o1 = models.IntegerField(choices=O1_HOLE_CHOICES,
                                      default=70)
    # which phase plate are we using
    php = models.IntegerField(choices=PHP_CHOICES,
                                      default=0)
    # phase plate starting position
    php_position_start = models.IntegerField(default=-1, null=True)

    # movies per phase plate position
    php_periodicity    = models.IntegerField(default=-1, null=True)

    def save(self, *args, **kwargs):
        #create project name
        if self.dose_in_last_fraction == -1:
            self.dose_per_fraction = \
                (self.total_dose_per_movie) / self.number_of_fractions
        else:
            # if input in e/px
            # self.number_of_fractions * self.sampling_rate * self.samplig_rate
            self.dose_per_fraction = \
                (self.total_dose_per_movie - self.dose_in_last_fraction)\
                /(self.number_of_fractions -1)
        super(Acquisition2, self).save(*args, **kwargs)

    def __str__(self):  #For Python 2, use __str__ on Python 3
        try:
            return "user=%s, sample=%s, date=%s" % \
                   (self.acquisition.user,
                    self.acquisition.sample,
                    self.acquisition.date.strftime('%Y-%m-%d %H:%M'))
        except:
            return "sample=%s, date=%s"%(
                self.acquisition.sample,
                self.acquisition.date.strftime('%Y-%m-%d %H:%M'))
