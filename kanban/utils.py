import json
from django.core.serializers import serialize as django_serialize
from django.db.models import Model
from django.http import HttpResponse
from django.views.generic import TemplateView


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

    def convert_context_to_json(self, context):
        def serialize(obj):
            if type(obj) == dict:
                for key, value in obj.iteritems():
                    obj[key] = serialize(value)
                return obj
            elif hasattr(obj, '__iter__'):
                result = []
                for item in obj:
                    result.append(serialize(item))
                return result
            elif isinstance(obj, Model) and  hasattr(obj, 'dictify'):
                return obj.dictify()
            else:
                return django_serialize('python', [obj])[0]

        return json.dumps(serialize(context))


class JSONView(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)