# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from invoice.models import Concept, Invoice, InvoiceLine
# Register your models here.



class ConceptAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit_price_cnb',
                                  'unit_price_csic',
                                  'unit_price_universidad',
                                  'unit_price_empresa'
                    )

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'ordered_by', 'creation_date')

admin.site.register(Concept, ConceptAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceLine)
