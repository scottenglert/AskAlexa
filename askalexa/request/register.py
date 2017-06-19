from askalexa.exceptions import UnknownRequestType, RequestError

class RequestRegister(type):
    '''
    Request registration metaclass. This class is used to automacally register
    request classes that use this as it's metaclass. The request class must
    set the "request_type" class variable to match the one in the Alexa
    request JSON. The class must also have a "create_from_json" class method
    that is used to construct the request with JSON data object.
    '''

    registered_request_classes = {}

    def __new__(cls, name, bases, attrs):
        request_class = super(RequestRegister, cls).__new__(cls, name, bases, attrs)

        request_type = attrs.get('request_type')
        if request_type is not None:
            cls.registered_request_classes[request_type] = request_class

        return request_class

    @classmethod
    def create_from_json(cls, request_json):
        '''
        Create a request instance from the given request JSON data.
        '''
        try:
            request_type = request_json['type']
        except KeyError:
            raise RequestError('Unable to get request type from json data.')

        try:
            request_class = cls.registered_request_classes[request_type]
        except KeyError:
            raise UnknownRequestType('Invalid request type: {0}'.format(request_type))

        return request_class.create_from_json(request_json)

    @classmethod
    def registered_request_types(cls):
        return sorted(cls.registered_request_classes.keys())