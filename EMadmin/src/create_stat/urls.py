from django.conf.urls import url
from . import views

app_name = 'create_stat'

urlpatterns = [
    url(r'^all/$', views.create_all_statistics, name='all'),
    url(r'^create_resolution_plot/$', views.create_resolution_plot, name='create_resolution_plot'),
]
