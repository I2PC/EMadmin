from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^all/$', views.create_all_statistics, name='all'),
]
