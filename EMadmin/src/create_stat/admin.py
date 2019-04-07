# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from create_stat.models import Statistics

class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('acquisition','numberMovies', 'averageResolution')

# Register your models here.
admin.site.register(Statistics,StatisticsAdmin )


