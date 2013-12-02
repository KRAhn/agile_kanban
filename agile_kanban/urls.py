from django.conf.urls import patterns, include, url
from kanban.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', HomePageView.as_view()),
    url(r'^iteration/now/$', IterationDetailView.as_view()),
    url(r'^iteration/now/add/$', TaskAddView.as_view()),
    url(r'^task/(\d+)/edit/$', TaskEditView.as_view()),
)
