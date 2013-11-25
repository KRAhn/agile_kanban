from django.views.generic import TemplateView
from kanban.models import Status, Task
from kanban.utils import JSONView


class HomePageView(TemplateView):

    template_name = "home.html"


class IterationDetailView(JSONView):

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        tasks = {status.name:Task.objects.filter(status=status)
                 for status in Status.objects.all()}
        context['tasks'] = tasks
        return context