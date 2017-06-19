'''
===================
Base Request Module
===================

This module holds classes that are used as a base for all request types.

Request classes are automacally registered by using the RequestRegister
metaclass. All request classes should inherit from the BaseRequest class
and set the request_type class variable to the respective Alexa request
type found in the JSON request data.
'''

from askalexa.request.register import RequestRegister

class BaseRequest(object):
    '''
    Base class for all requests. You must inherit from this class and set the
    request_type class variable for each concrete request type. If needed, you
    should implement your own "create_from_json" class method to build your
    request instance.
    '''
    __metaclass__ = RequestRegister

    request_type = None

    def __init__(self, request_id, locale, timestamp, **kwargs):
        '''
        All requests have a requestID, locale, and timestamp
        '''
        self._request_id = request_id
        self._locale = locale
        self._timestamp = timestamp

    @classmethod
    def create_from_json(cls, request_json, **kwargs):
        '''
        Inherited request classes should call this base class method to get the
        base request data from the JSON object.
        '''
        request_id = request_json['requestId']
        locale = request_json['locale']
        timestamp = request_json['timestamp']
        return cls(request_id=request_id, locale=locale, timestamp=timestamp, **kwargs)

    @property
    def request_id(self):
        '''
        Represents a unique identifier for the specific request.
        '''
        return self._request_id
    
    @property
    def locale(self):
        '''
        A string indicating the users locale. For example: en-US.
        '''
        return self._locale

    @property
    def timestamp(self):
        '''
        Provides the date and time when Alexa sent the request as an ISO 8601
        formatted string.
        '''
        return self._timestamp