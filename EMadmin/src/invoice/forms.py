from django import forms
from create_proj.models import Acquisition
from datetime import datetime, timedelta
from models import Concept, TYPE_CHOICES_SET
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings
from django.utils import timezone

#kill port sudo lsof -t -i tcp:8000 | xargs kill -9
class InvoiceForm1(forms.Form):
    def __init__(self, *args, **kwargs):
         # if 'orderedBy' in kwargs:
         #     orderedBy = kwargs.pop('orderedBy')
         # else:
         #     orderedBy = False
         # if 'type' in kwargs:
         #     type = kwargs.pop('type')
         # else:
         #     type = 'cnb'
         super(InvoiceForm1, self).__init__(*args, **kwargs)
         # if orderedBy:
         #     self.fields['orderedBy'].initial = orderedBy
         self.fields['orderedBy'].queryset =  \
              User.objects.all().order_by('name')
         # self.fields['type'] = type


         ##project   = forms.ModelChoiceField(queryset=None, initial=0)
    orderedBy = forms.ModelChoiceField(queryset=None)
    type = forms.ChoiceField(choices=TYPE_CHOICES_SET, initial='cnb')
    startDate = forms.DateField(widget = forms.SelectDateWidget, initial=timezone.now)
    endDate = forms.DateField(widget = forms.SelectDateWidget, initial=timezone.now)

class InvoiceForm2(forms.Form):
    def __init__(self, *args, **kwargs):
        """Get projects done last week by current user"""
        if 'invoice' in kwargs:
            invoice = kwargs.pop('invoice')
        else:
            invoice = None
            orderedBy = False
        super(InvoiceForm2, self).__init__(*args, **kwargs)
        initialConcep=[0]*settings.NUMBERCONCEPTS
        initialQuantity=[0]*settings.NUMBERCONCEPTS
        initRange=1
        querySet= Concept.objects.filter().order_by('name')
        if invoice is not None:
            i = initRange
            for line in invoice.items.all():
                self.fields['c_%03d'%i] = forms.ModelChoiceField(
                    queryset=querySet,  initial=line.concept.id, label="%02d"%i)
                self.fields['n_%03d'%i] = forms.IntegerField(initial=line.quantity,
                                                             label="")
                i +=1
            initRange = i
        for i in range(initRange,settings.NUMBERCONCEPTS):
            self.fields['c_%03d'%i] = forms.ModelChoiceField(
                queryset=querySet,  initial=0, label="%02d"%i)
            self.fields['n_%03d'%i] = forms.IntegerField(initial=0, label="")
