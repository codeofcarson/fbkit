class json(object):
    pass

class Proxy(object):
    """Represents a "namespace" of Facebook API calls."""

    def __init__(self, client):
        self._client = client

    def __call__(self, method=None, args=None, signed=False):
        # for Django templates
        if method is None:
            return self
        return self._client('%s.%s' % (self._name, method), args, signed=signed)

def build_proxy(namespace, bindings, klass=Proxy):
    def __fixup_param(name, klass, options, param):
        default = options.get('default', None)
        if param is None:
            if klass is list and default:
                param = default[:]
            else:
                param = default
        if klass is json and isinstance(param, (list, dict)):
            param = simplejson.dumps(param)
        return param

    def __generate_method(namespace, method_name, param_data):
        # This method-level option forces the method to be signed rather than using
        # the access_token
        signed = False
        if 'signed' in param_data:
            signed = True
            param_data.remove('signed')
        required = [x for x in param_data if not x[2].get('optional', False) and 'default' not in x[2]]

        def facebook_method(self, *args, **kwargs):
            params = {}
            for i, arg in enumerate(args):
                params[param_data[i][0]] = arg
            params.update(kwargs)
            for param in required:
                if param[0] not in params:
                    raise TypeError("missing parameter %s" % param[0])
            for name, klass, options in param_data:
                if name in params:
                    params[name] = __fixup_param(name, klass, options, params[name])
            return self(method_name, params, signed=signed)
        facebook_method.__name__ = method_name
        facebook_method.__doc__ = "Facebook API call. See http://developers.facebook.com/documentation.php?v=1.0&method=%s.%s" % (namespace, method_name)

        return facebook_method
    properties = {
        '_name': 'facebook.%s' % namespace,
    }
    for method, param_data in bindings.iteritems():
        properties[method] = __generate_method(namespace, method, param_data)
    proxy = type('%sProxy' % namespace.title(), (klass,), properties)
    return proxy

