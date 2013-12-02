#-*-coding:utf8-*-
from django.http import HttpResponseNotFound, Http404, HttpResponseBadRequest
from django.views.generic import TemplateView, CreateView
from kanban.models import Status, Task, Iteration
from kanban.utils import JSONView, JSONResponseMixin


class HomePageView(TemplateView):
    template_name = "home.html"


class IterationDetailView(JSONView):
    def get_context_data(self):
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


class TaskEditView(JSONView):
    def get_context_data(self, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise Http404()

        task.title = self.get_parameter('title')
        task.description = self.get_parameter('description')
        task.author = self.get_parameter('author')
        try:
            task.status = Status.objects.get(name=self.get_parameter('status'))
        except Status.DoesNotExist:
            return HttpResponseBadRequest()
        task.save()
        return dict(code='OK')


class TaskAddView(JSONView):
    def get_context_data(self):
        title = self.get_parameter('title')
        author = self.get_parameter('author')
        description = self.get_parameter('description')
        status_name = self.get_parameter('status_name')
        created_time = self.get_parameter('created_time')
        try:
            status = Status.objects.get(name=status_name)
        except Status.DoesNotExist:
            return HttpResponseNotFound()

        iteration = Iteration.objects.order_by('-id')[0]

        task = Task.objects.create(
            title=title,
            author=author,
            description=description,
            status=status,
            created_time=created_time,
            iteration=iteration
        )

        return dict(id=task.id)