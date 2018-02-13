from django.conf.urls import url
import views

urlpatterns = [
    url(r'^create_invoice/(?P<idacquisition>[\w\-]+)/$', views.create_invoice,
        name='create_invoice'),
#    url(r'^create_invoice/$', views.create_invoice,
#        name='create_invoice'),
]
