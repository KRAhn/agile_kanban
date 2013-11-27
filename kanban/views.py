#-*-coding:utf8-*-
from django.views.generic import TemplateView
from kanban.models import Status, Task, Iteration
from kanban.utils import JSONView


class HomePageView(TemplateView):
    template_name = "home.html"


class IterationDetailView(JSONView):
    def get_context_data(self, **kwargs):
        try:
            iteration = Iteration.objects.order_by('-id')[0]
        except IndexError:
            iteration = Iteration.objects.create(goal=u'목표를 입력하세요')
        return dict(taskGroups=[dict(id=status.id,
                                     name=status.name,
                                     displayName=status.get_name_display(),
                                     tasks=Task.objects.filter(status=status,
                                                               iteration=iteration))
                                for status in Status.objects.all()],
                    goal=iteration.goal)