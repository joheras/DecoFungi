"""cv_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import fungi_classification.views
import statisticalAnalysis.views

urlpatterns = [

    url(r'^$', fungi_classification.views.index, name='index'),
    # URLs for statistical Analysis
    url(r'^statisticalAnalysis/$', statisticalAnalysis.views.simple_upload),

    url(r'^fungi_classification/predictFungiClass/$', fungi_classification.views.predictFungiClassUsingOverfeatViewGUI,
        name='predictOne'),
    url(r'^fungi_classification/predictFungiClass/result/$',
        fungi_classification.views.predictFungiClassUsingOverfeatViewGUIResult,
        name='result'),
    url(r'^fungi_classification/predictFungiClass/zip/$',
        fungi_classification.views.predictFungiClassUsingOverfeatViewZIPGUI, name='predictZip'),
    url(r'^fungi_classification/predictFungiClassControl/$',
        fungi_classification.views.predictFungiClassUsingOverfeatViewControlGUI, name='predictControl'),
    url(r'^fungi_classification/predictFungiClassControl/zip/$',
        fungi_classification.views.predictFungiClassUsingOverfeatViewZIPControlGUI, name='predictZipControl'),

    url(r'^fungi_classification/about/$',
        fungi_classification.views.about, name='about'),
    url(r'^fungi_classification/tutorial/$',
        fungi_classification.views.tutorial, name='tutorial'),

    # URLs for fungi classification

    url(r'^fungi_classification/predictFungiClass/examples/(?P<num>\w{0,50})$',
        fungi_classification.views.predictFungiClassUsingOverfeatViewExamples, name='examples'),

    url(r'^fungi_classification/predictFungiClassControl/examples/(?P<num>\w{0,50})$',
        fungi_classification.views.predictFungiClassUsingOverfeatViewControlExamples, name='examplesControl'),

    url(r'^random/(?P<num>\w{0,1000})$',
        fungi_classification.views.randomGenerator, name='random'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
