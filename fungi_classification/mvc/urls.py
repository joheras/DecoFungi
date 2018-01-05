"""Configuracion URL de la clase MVC
"""
from django.conf.urls import url
from . import views
from mvc.views import index, contacto

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^contacto/', views.contacto, name='contacto'),
	url(r'^gracias/', views.gracias, name='gracias'),
    url(r'^contacto2/', views.contacto2, name='contacto2'),
	url(r'^gracias2/', views.gracias2, name='gracias2'),
	url(r'^contacto3/', views.contacto3, name='contacto3'),
	url(r'^gracias3/', views.gracias3, name='gracias3'),
	url(r'^contacto4/', views.contacto4, name='contacto4'),
	url(r'^gracias4/', views.gracias4, name='gracias4'),
]


