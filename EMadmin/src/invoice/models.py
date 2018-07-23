# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from create_proj.models import Acquisition
from django.conf import settings
from decimal import Decimal
import datetime

# Create your models here.

TYPE_CHOICES = {'cnb': 'cnb',
           'csic': 'csic',
           'universidad': 'universidad',
           'empresa': 'empresa'}
TYPE_CHOICES_SET = []
for k, v in TYPE_CHOICES.iteritems():
    TYPE_CHOICES_SET.append((v, k))

CONCEPT_CHOICES = {'presupuesto': 'presupuesto',
                   'notificacion': 'notificación',
                   'cargo': 'cargo'
}
CONCEPT_CHOICES_SET = []
for k, v in CONCEPT_CHOICES.iteritems():
    CONCEPT_CHOICES_SET.append((v, k))

class Invoice(models.Model):

    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True, blank=True, db_index=True,
                                   verbose_name='ordered by', 
                                   related_name='orders', 
                                   help_text='user who sent this order out')

    #acquisition   = models.OneToOneField(Acquisition)
    startDate = models.DateField(default=datetime.date.today)
    endDate   = models.DateField(default=datetime.date.today)
    creation_date = models.DateField(blank=True, null=True, auto_now_add=True )
    type = models.CharField(max_length=11, choices=TYPE_CHOICES_SET, default='cnb')
    concept = models.CharField(max_length=11, choices=CONCEPT_CHOICES_SET, default='cargo')


    def total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total = total + item.total()
        return total

class Concept(models.Model):
    name = models.CharField(max_length=60, unique=True,
        help_text='short descriptive name of this product')
    unit_price_cnb = models.DecimalField(max_digits=8, decimal_places=2)
    unit_price_csic = models.DecimalField(max_digits=8, decimal_places=2)
    unit_price_universidad = models.DecimalField(max_digits=8, decimal_places=2)
    unit_price_empresa = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        return self.name

class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items')
    concept = models.ForeignKey(Concept)
    quantity = models.IntegerField(null=True)
    unit_price = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    
    def total(self):
        total = Decimal(str(self.unit_price * self.quantity))
        return total.quantize(Decimal('0.01'))
