# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from create_proj.models import Acquisition
from django.conf import settings
from decimal import Decimal

# Create your models here.

class Invoice(models.Model):

    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True, blank=True, db_index=True,
                                   verbose_name='ordered by', 
                                   related_name='orders', 
                                   help_text='user who sent this order out')

    acquisition   = models.OneToOneField(Acquisition)
    creation_date = models.DateField(blank=True, null=True, auto_now_add=True )

    def total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total = total + item.total()
        return total

class Concept(models.Model):
    name = models.CharField(max_length=60, unique=True,
        help_text='short descriptive name of this product')
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

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
