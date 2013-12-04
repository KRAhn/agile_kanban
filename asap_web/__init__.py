# -*- coding:utf8 -*-
import datetime
import random
import hashlib
import urllib
import json
import string
from django.core.serializers import serialize as django_serialize
from django.db.models import Model
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from asap_web.exceptions import *
from asap_web.models import AccessLog


class AcurosView(object):
    login_required = False
    accept_log = True
    request = None

    def __call__(self, request, *args, **kwargs):
        def main():
            if 'HTTP_X_REAL_IP' in request.META:
                request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
            AcurosView.request = request
            log_request()
            return process_request()

        def log_request():
            if not request.session.has_key('trace_key'):
                randomstring = list(
                    '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-./:;<=>?@[\]^_`{|}~')
                random.shuffle(randomstring)
                request.session['trace_key'] = hashlib.sha256(
                    ''.join(randomstring)).hexdigest()
            if self.accept_log:
                access_log = AccessLog.objects.create(
                    trace_key=request.session[
                        'trace_key'], path=request.META['PATH_INFO'],
                    query_string=urllib.unquote(request.META['QUERY_STRING']), ip=request.META['REMOTE_ADDR'],
                    referer=urllib.unquote(request.META.get('HTTP_REFERER', '')),
                    user=request.user if request.user.is_authenticated() else None)
                request.session['access_stack'] = request.session.get(
                    'access_stack', []) + [access_log.id]

        def process_request():
            try:
                if self.login_required == True and not request.user.is_authenticated():
                    if request.is_ajax():
                        raise NoLoginError('')
                    else:
                        return HttpResponseRedirect('/member/login/?next=%s' % request.META['PATH_INFO'])
                else:
                    _call_preprocessor()
                    return _call_proper_request_processor()
            except AcurosCustomError, exception:
                return _error_response(exception)

        def _call_preprocessor():
            self.args = list(args)
            if hasattr(self, 'preprocess'):
                preprocess_result = self.preprocess(request, *args, **kwargs)
                if type(preprocess_result) == tuple:
                    self.args = preprocess_result
                else:
                    self.args = [preprocess_result]

        def _call_proper_request_processor():
            requested_method = self.request.method.lower()
            if self.request.is_ajax() and \
                    hasattr(self, 'process_ajax_%s_request' % requested_method):
                method_name = 'process_ajax_%s_request' % requested_method
            else:
                method_name = 'process_%s_request' % requested_method
            if hasattr(self, method_name):
                if hasattr(self, 'preprocess'):
                    result = getattr(self, method_name)(request, *self.args)
                else:
                    result = getattr(self, method_name)(request, *self.args, **kwargs)
                if not isinstance(result, HttpResponse):
                    result = serialize(result)
                    result = HttpResponse(result, mimetype='application/json')
                return result
            else:
                raise UnsupportedMethodError(
                    "The method '%s' is not valid method for this request." % (self.request.method))

        def _error_response(exception):
            message = exception.message
            if request.is_ajax():
                return HttpResponse(json.dumps(dict(status=dict(code=str(exception.__class__.__name__), reason=exception.message.encode('utf8')))), mimetype='application/json')
            else:
                return render(request, 'error.html', {'error_message': message}, status=500)

        return main()

    def __getattr__(self, name):
        return getattr(self.request, name)

    def get_file_parameter(self, parameter_name, default=None, is_required=True):
        return self.get_parameter(parameter_name, parameter_pool=self.request.FILES, default=default, is_required=is_required)

    def get_post_parameter(self, parameter_name, default="", is_required=True, type=str):
        return self.get_parameter(parameter_name, parameter_pool=self.request.POST, default=default, is_required=is_required)

    def get_get_parameter(self, parameter_name, default="", is_required=True, type=str):
        return self.get_parameter(parameter_name, parameter_pool=self.request.GET, default=default, is_required=is_required)

    def get_parameter(self, parameter_name, default="", is_required=True, error_message=u"올바른 요청이 아닙니다."):
        def get_default_parameter():
            if is_required:
                raise NoParameterError(parameter_name)
            else:
                if default == "":
                    return parameter
                else:
                    return default

        parameter = self.request.REQUEST.get(parameter_name, "")
        if parameter == "":
            parameter = get_default_parameter()

        return parameter


def serialize(context):
    def deep_serialize(obj):
        if type(obj) == dict:
            for key, value in obj.iteritems():
                obj[key] = deep_serialize(value)
            return obj
        elif hasattr(obj, '__iter__'):
            result = []
            for item in obj:
                result.append(deep_serialize(item))
            return result
        elif isinstance(obj, Model) and hasattr(obj, 'dictify'):
            return obj.dictify()
        elif type(obj) in (unicode, str, int, float):
            return obj
        elif type(obj) == datetime.datetime:
            return str(obj)
        else:
            return django_serialize('python', [obj])[0]

    return json.dumps(deep_serialize(context))


def generate_username_and_password():
    _LOWERCASE = ''.join(string.ascii_lowercase)
    _ALPHA_DIGIT = ''.join(
        [string.ascii_lowercase, string.ascii_uppercase, string.digits])
    USERNAME_LENGTH = 8
    PASSWORD_LENGTH = 10

    return  ''.join([''.join(random.sample(_LOWERCASE, 1)), ''.join(random.sample(_ALPHA_DIGIT, USERNAME_LENGTH - 1))]),\
            ''.join([''.join(random.sample(_LOWERCASE, 1)), ''.join(
                random.sample(_ALPHA_DIGIT, PASSWORD_LENGTH - 1))])


def to_pretty_time(event_time):
    delta = datetime.datetime.now() - event_time
    if delta < datetime.timedelta(seconds=10):
        return u'방금'
    elif delta < datetime.timedelta(minutes=1):
        return u'몇십 초 전'
    elif delta < datetime.timedelta(hours=1):
        return u'%d분 전' % (delta.seconds // 60)
    elif delta < datetime.timedelta(days=1):
        return u'%d시간 전' % (delta.seconds // 60 // 60)
    elif delta < datetime.timedelta(days=7):
        return u'%d일 전' % delta.days
    elif delta < datetime.timedelta(days=60):
        return u'%d주 전' % (delta.days // 7)
    elif delta < datetime.timedelta(days=365):
        return u'%d달 전' % (delta.days // 30)
    else:
        return u'머나먼 시간'


def make_cache_key(key, *args):
    from django.db import models

    def stringify(*args):
        result = []
        for arg in args:
            if type(arg) == str:
                result.append(arg.decode('utf8'))
            elif type(arg) == unicode:
                result.append(arg)
            elif isinstance(arg, models.Model):
                model_id = getattr(arg, 'id') or 0
                result.append(u'%s#%d' % (arg.__class__.__name__, model_id))
            elif type(arg) == dict:
                result.append(u'|'.join(u'%s||%s' % (stringify(key), stringify(value))
                                        for key, value in arg.iteritems()))
            elif hasattr(arg, '__iter__'):
                for item in arg:
                    result.append(stringify(item))
            else:
                result.append(unicode(arg))
        return u','.join(result)
    return u'%s-%s' % (key, stringify(*args))


def is_mobile(user_agent):
    mobile_user_agent_keywords = ['Windows Phone', 'Android', 'iPhone',
                                  'iPad', 'SymbianOS', 'Nokia', 'BlackBerry', 'Bada']
    for mobile_user_agent_keyword in mobile_user_agent_keywords:
        if user_agent.find(mobile_user_agent_keyword) >= 0:
            return True
    return False
