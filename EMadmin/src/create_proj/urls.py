from django.conf.urls import url
from . import views

app_name = 'create_proj'

urlpatterns = [
    url(r'^add_acquisition$', views.add_acquisition, name='add_acquisition'),
    url(r'^add_acquisition2$', views.add_acquisition2, name='add_acquisition2'),
    url(r'^getWorkflow/(?P<name>[\w\ ]{0,128})/', views.getWorkflow, name='getWorkflow'),
]
