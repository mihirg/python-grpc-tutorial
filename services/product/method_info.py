class MethodInfo(object):

    def __init__(self, name, url, request_clas, response_cls):
        self.name = name
        self.url = url
        self.request_cls = request_clas
        self.response_cls = response_cls
