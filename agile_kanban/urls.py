from django.conf.urls import patterns, include, url
from kanban.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^iteration/now/$', IterationDetailView.as_view(),
        name='iteration_detail')
)
