
class TypeformException(Exception):
    message = None
    code = None

    def __init__(self, exc={'message': None, 'code': None}):
        self.message = exc['message']
        self.code = exc['code']

    def __str__(self):
        return self.msg, self.code

