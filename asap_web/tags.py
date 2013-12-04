from django.template import Node


class AcurosTemplateTag(Node):
    parameter_infos = ()

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def get_parameters(self, args, kwargs, context):
        out_args = [arg.resolve(context) for arg in args]
        out_kwargs = dict([(k, v.resolve(context)) for k, v in kwargs.items()])
        for x in xrange(len(out_args)):
            if out_args[x] == '':
                out_args[x] = self.parameter_infos[x]['default']
        return out_args + [out_kwargs.get(parameter_info['name'], context.get(parameter_info['name']) or context['request'].REQUEST.get(parameter_info['name']) or parameter_info.get('default')) for parameter_info in self.parameter_infos[len(out_args):]]


def parse_args_kwargs(parser, bits):
    args = []
    kwargs = {}

    bits = iter(bits)
    for bit in bits:
        for arg in bit.split(","):
            if '=' in arg:
                k, v = arg.split('=', 1)
                k = k.strip()
                kwargs[k] = parser.compile_filter(v)
            elif arg:
                args.append(parser.compile_filter(arg))
    return args, kwargs
