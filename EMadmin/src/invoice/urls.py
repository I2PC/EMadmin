from django.conf.urls import url
import views

urlpatterns = [
    url(r'^create_invoice/(?P<invoiceid>[\w\-]+)/$', views.create_invoice,
        name='create_invoice_parameter'),
    url(r'^create_invoice/$', views.create_invoice, name='create_invoice'),
]
