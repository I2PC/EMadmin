# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Register your models here.
from django.contrib import admin
from models import Microscope, Acquisition, Workflow, Acquisition2

class AcquisitionAdmin(admin.ModelAdmin):
    list_display = ('noScipionProject','user', 'workflow', 'sample',
                    'date', 'shiftLength', 'projname', 'backupPath', 'microscope')

admin.site.register(Acquisition, AcquisitionAdmin)
admin.site.register(Acquisition2)
admin.site.register(Workflow)
admin.site.register(Microscope)
