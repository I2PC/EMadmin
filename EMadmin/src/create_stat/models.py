# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from create_proj.models import Acquisition


class Statistics(models.Model):
    acquisition = models.OneToOneField(Acquisition)
    numberMovies = models.IntegerField(default=-1)
    averageResolution = models.FloatField(default=-1)
    resolutionData = models.TextField()
    defocusData = models.TextField()

    def __str__(self):
        return "stat of %s"%self.acquisition.projname


