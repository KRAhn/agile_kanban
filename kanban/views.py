from django.views.generic import TemplateView
from kanban.models import Status, Task
from kanban.utils import JSONView


class HomePageView(TemplateView):

    template_name = "home.html"


class IterationDetailView(JSONView):

    def get_context_data(self, **kwargs):
        return [dict(id=status.id,
                     name=status.name,
                     displayName=status.get_name_display(),
                     tasks=Task.objects.filter(status=status))
                for status in Status.objects.all()]
