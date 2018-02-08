from django import forms
from create_proj.models import Acquisition
from datetime import datetime, timedelta
from models import Concept
from django.contrib.auth import get_user_model
User = get_user_model()

#kill port sudo lsof -t -i tcp:8000 | xargs kill -9
class InvoiceForm1(forms.Form):
    def __init__(self, *args, **kwargs):
         """Get projects done last week by current user"""
         super(InvoiceForm1, self).__init__(*args, **kwargs)
         last_mounth = datetime.today() - timedelta(days=30)
         self.fields['project'].queryset =  \
             Acquisition.objects.filter(
                 date__gte=last_mounth).order_by('-date')
         self.fields['orderedBy'].queryset =  \
             User.objects.all().order_by('name')

    project   = forms.ModelChoiceField(queryset=None, initial=0)
    orderedBy = forms.ModelChoiceField(queryset=None, initial=0)

class InvoiceForm2(forms.Form):
    def __init__(self, *args, **kwargs):
         """Get projects done last week by current user"""
         super(InvoiceForm2, self).__init__(*args, **kwargs)
    concept_1   = forms.ModelChoiceField(
            queryset=Concept.objects.filter().order_by('unit_price'),
            initial=0)
    concept_2   = forms.ModelChoiceField(
            queryset=Concept.objects.filter().order_by('unit_price'),
            initial=0)
    concept_3   = forms.ModelChoiceField(
            queryset=Concept.objects.filter().order_by('unit_price'), initial=0)
    concept_4   = forms.ModelChoiceField(
            queryset=Concept.objects.filter().order_by('unit_price'), initial=0)
    concept_5   = forms.ModelChoiceField(
            queryset=Concept.objects.filter().order_by('unit_price'), initial=0)
    concept_6   = forms.ModelChoiceField(
            queryset=Concept.objects.filter().order_by('unit_price'), initial=0)
    concept_7   = forms.ModelChoiceField(
            queryset=Concept.objects.filter().order_by('unit_price'), initial=0)
    concept_8   = forms.ModelChoiceField(
            queryset=Concept.objects.filter().order_by('unit_price'), initial=0)

class InvoiceForm3(forms.Form):
    def __init__(self, *args, **kwargs):
         """Get projects done last week by current user"""
         super(InvoiceForm3, self).__init__(*args, **kwargs)

    n1 = forms.IntegerField(initial=0, label="")
    n2 = forms.IntegerField(initial=0, label="")
    n3 = forms.IntegerField(initial=0, label="")
    n4 = forms.IntegerField(initial=0, label="")
    n5 = forms.IntegerField(initial=0, label="")
    n6 = forms.IntegerField(initial=0, label="")
    n7 = forms.IntegerField(initial=0, label="")
    n8 = forms.IntegerField(initial=0, label="")
