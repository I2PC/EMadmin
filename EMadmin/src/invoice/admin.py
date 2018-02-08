# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Concept, Invoice, InvoiceLine
# Register your models here.



class ConceptAdmin(admin.ModelAdmin):
    list_display = ('name','unit_price')

admin.site.register(Concept, ConceptAdmin)
admin.site.register(Invoice)
admin.site.register(InvoiceLine)
