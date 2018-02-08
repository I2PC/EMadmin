# tutorial/tables.py
import django_tables2 as tables
from create_proj.models import Acquisition
from django.conf import settings

class ProjectsTable(tables.Table):
    session_id = tables.TemplateColumn( '{{record.id}}', order_by=('projname'))

    go_to_Html_Summary = tables.TemplateColumn('<a href="http://%s/%s/{{record.projname}}">'
                                     '{{record.projname}}</a>'%
                                     (settings.PUBLISHURL, settings.PUBLISHUSER), order_by=('projname'))

    get_Report = tables.TemplateColumn('<a href={% url "create_report:create_report_latex" record.id %}>'
                                       '{{record.projname}}</a>',
                                       order_by=('projname'))

    produce_invoice = tables.TemplateColumn('<a href={% url "invoice:create_invoice" record.id %}>'
                                       '{{record.projname}}</a>',
                                       order_by=('projname'))


    #tables.TemplateColumn('{{record.projname}}', order_by=('projname'))
    class Meta:
        #model = Acquisition
        attrs = {'class': 'paleblue'}
