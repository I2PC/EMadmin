from django.conf.urls import url
import invoice.views as views

app_name = 'create_invoice'

urlpatterns = [
    url(r'^create_invoice/(?P<invoiceid>[\w\-]+)/$', views.create_invoice,
        name='create_invoice_parameter'),
    url(r'^create_invoice/$', views.create_invoice, name='create_invoice'),
]
