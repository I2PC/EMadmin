# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from forms import InvoiceForm1, InvoiceForm2
from django.contrib.auth import get_user_model
# Create your views here.
from create_proj.models import Acquisition
from models import Invoice, InvoiceLine, Concept
import jinja2, os
from django.conf import settings
import unidecode
from django.http import HttpResponse
from models import Concept, TYPE_CHOICES

User = get_user_model()


def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)

    return (
        '{method} HTTP/1.1\n'
        'Content-Length: {content_length}\n'
        'Content-Type: {content_type}\n'
        '{headers}\n\n'
        '{body}'
    ).format(
        method=request.method,
        content_length=request.META['CONTENT_LENGTH'],
        content_type=request.META['CONTENT_TYPE'],
        headers=headers,
        body=request.body,
)


import re

def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless ',
        '>': r'\textgreater ',
    }
    regex = re.compile('|'.join(re.escape(unicode(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)

def create_report_latex(invoice):
    # init template procesor jinja2 for
    latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('/'))
    )

    latexTemplateFile = settings.LATEX_INVOICE_TEMPLATE
    latexLogoFile = settings.LATEX_REPORT_TEMPLATE_ICON
    template = latex_jinja_env.get_template(os.path.realpath(latexTemplateFile))

    options = {}
    # Header
    #acquisition = invoice.acquisition
    options['projectName'] = invoice.startDate.strftime('%d-%m-%Y') + "/" + invoice.endDate.strftime('%d-%m-%Y')
    options['invoicenum'] = invoice.id
    options['companyname'] = settings.COMPNAME
    orderedBy = invoice.ordered_by.name + "\\\\" + \
                invoice.ordered_by.profile.institution
    options['orderedby'] = orderedBy

    concepts=""
    for line in invoice.items.all():
        concepts += "%s & %8.2f\\texteuro & %d & %8.2f\\texteuro\\\\"%(
            tex_escape(line.concept.name),
                                              line.unit_price,
                                    line.quantity, line.total())
    options['concepts'] = concepts
    options['total'] = invoice.total()

    # if project exists compile data in scipionuserdata/project/Logs
    # otherwise use /tmp
    # out_dir=os.path.join(settings.SCIPIONUSERDATA, "projects",
    #                      invoice.acquisition.projname, "Tmp")
    # if os.path.isdir(out_dir):
    #     pass
    # else:
    out_dir = "/tmp"
    out_file_root=os.path.join(out_dir,"temp")
    renderer_template = template.render(**options)
    with open(out_file_root + ".tex", "w") as f:  # saves tex_code to outpout file
        f.write(unidecode.unidecode(renderer_template))

    os.system('pdflatex -output-directory %s %s'%(out_dir, out_file_root))
    with open(os.path.join(out_dir, out_file_root + ".pdf"), 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.close()
    return HttpResponse("Can not create invoice")


@staff_member_required
def create_invoice(request, invoiceid=-1):
    #acquisition = Acquisition.objects.get(pk=idacquisition)
    if request.method == 'POST':
        form1 = InvoiceForm1(request.POST)
        form2 = InvoiceForm2(request.POST)
        if form1.is_valid() and form2.is_valid():
            # process form1
            data1 = form1.cleaned_data
            user = data1['orderedBy']
            type = data1['type']
            startDate = data1['startDate']
            endDate = data1['endDate']
            # check if there is an invoice for this adquisition
            # if there is update it
            invoice, created = Invoice.objects.get_or_create()
            invoice.ordered_by = user
            invoice.type = TYPE_CHOICES[type]
            invoice.startDate = startDate
            invoice.endDate = endDate
            invoice.save()
            # process form2
            data2 = form2.cleaned_data
            conceptDict={}
            quantityDict={}
            for k,v in data2.iteritems():
                key = int(k[2:])

                if k[0]=='n':
                    v = int(v)
                    if v == 0:
                        continue
                    quantityDict[key] = v
                elif k[0]=='c':
                    if v.name == "-----":
                        continue
                    conceptDict[key] = v
            print "AAAAAAAAAAa", quantityDict, conceptDict
            for k,v in   conceptDict.iteritems():
                invoiceline, created = InvoiceLine.objects.get_or_create(
                        invoice=invoice,
                        concept=v)
                invoiceline.quantity = quantityDict[k]
                if type == TYPE_CHOICES['cnb']:
                    invoiceline.unit_price = v.unit_price_cnb
                elif type == TYPE_CHOICES['csic']:
                    invoiceline.unit_price = v.unit_price_csic
                elif type == TYPE_CHOICES['universidad']:
                    invoiceline.unit_price = v.unit_price_universidad
                else:
                    invoiceline.unit_price = v.unit_price_empresa
                invoiceline.save()
            return create_report_latex(invoice)
        else:
            pass
    else:
        # check if there is an invoice for this project
        # if it does exists do not allow modifications
        # infor of ID.

        invoices = Invoice.objects.filter(pk=invoiceid)
        if invoices.exists():
            invoice = invoices[0]
            #orderedBy = invoice.ordered_by.id
        else:
            invoice = None
            #orderedBy = acquisition.user.id
        form1 = InvoiceForm1(auto_id=False)
        form2 = InvoiceForm2(auto_id=False, invoice=invoice)
    return render(request, 'invoice/invoice.html', {
                                                    'form1': form1,
                                                    'form2': form2,
                                                    })
