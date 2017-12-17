# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from create_proj.models import Acquisition


class Statistics(models.Model):
    acquisition     = models.OneToOneField()
    numberMovies    = models.IntegerField(default=-1)
    numberFractionsPerMovie = models.IntegerField(default=-1)
    # CTF related data
    averageResolution = models.FloatField(default=-1)
    averageAstigmatism = models.FloatField(default=-1)
    resolutionData = models.TextField()
    defocusData = models.TextField()
    astigmaticData = models.TextField()
    # I do not think gain Data is available as a Scipion
    # object but who knows in the future
    gainData = models.TextField()
    # Movie alignment data
    alignmentShiftX = models.TextField()
    alignmentShiftY = models.TextField()


    def __str__(self):
        return "stat of %s"%self.acquisition.projname


