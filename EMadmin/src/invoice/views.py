# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from forms import InvoiceForm1, InvoiceForm2, InvoiceForm3
# Create your views here.
from create_proj.models import Acquisition

@staff_member_required


def create_invoice(request, idacquisition):
    #acquisition = Acquisition.objects.get(pk=idacquisition)
    if request.method == 'POST':
        form = InvoiceForm1(request)
        if form.is_valid():
            pass
        else:
            pass
    else:
        form1 = InvoiceForm1(auto_id=False)
        form2 = InvoiceForm2(auto_id=False)
        form3 = InvoiceForm3(auto_id=False)
    return render(request, 'invoice/invoice.html', {'form1': form1,
                                                    'form2': form2,
                                                    'form3': form3})
