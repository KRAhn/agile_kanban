import datetime
import json
from django.core.serializers import serialize as django_serialize
from django.db.models import Model
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.generic import TemplateView, View


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

class JSONView(JSONResponseMixin, View):
    def get_parameter(self, name):
        value = self.request.REQUEST.get(name)
        if not value:
            return HttpResponseBadRequest()
        return value

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        return self.render_to_json_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        return self.render_to_json_response(context)