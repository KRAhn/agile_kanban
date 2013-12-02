from django.conf.urls import patterns, include, url
from kanban.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomePageView.as_view()),
    url(r'^iteration/now/$', IterationDetailView.as_view()),
    url(r'^iteration/now/add/$', TaskAddView.as_view()),
    url(r'^task/(\d+)/edit/$', TaskEditView.as_view()),
)
