from django.conf.urls import url
from . import views

app_name = 'create_report'

urlpatterns = [
    url(r'^create_report$', views.create_report, name='create_report'),
    url(r'^create_report_latex/(?P<idacquisition>[\w\-]+)/$', views.create_report_latex,
        name='create_report_latex'),
]
