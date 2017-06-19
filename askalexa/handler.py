'''
Alexa Request Event Handler Module
==================================
'''
import json
from askalexa.dispatcher import RequestDispatcher
from askalexa.response.package import ResponsePackage
from askalexa.response import ResponseBuilder
from askalexa.request.event import AlexaEvent
from askalexa.request import validation
from askalexa.exceptions import InvalidResponseError

class RequestEventHandler(object):
    '''
    This class handles an incoming request event and processes it.
    '''

    def __init__(self, request_data):
        '''
        Initialize the event handler with the raw json request data.
        '''
        self.request_data = request_data
        self.request_json = None

    def is_request_valid(self, certificate_url, signature):
        '''
        Returns True/False if the request is valid by checking the following:

        1. Validating the request timestamp
        2. Verifying the certificate is authentic
        3. Request matches the signature

        :returns: bool
        '''
        if self.request_json is None:
            self.request_json = json.loads(self.request_data)

        try:
            timestamp = self.request_json['request']['timestamp']
        except KeyError:
            return False

        if not validation.is_timestamp_valid(timestamp):
            return False

        return validation.is_request_certified(certificate_url, self.request_data, signature)

    def get_response(self):
        '''
        Process the incoming request. Requests are decoded and dispatched to
        the appropriate skill. The return is the response from the skill.
        '''
        if self.request_json is None:
            self.request_json = json.loads(self.request_data)

        alexa_event = AlexaEvent.create_from_json(self.request_json)
        alexa_response = RequestDispatcher.dispatch_request(alexa_event)
        if not isinstance(alexa_response, ResponseBuilder):
            raise InvalidResponseError('Response is not an instance of ResponseBuilder.')

        session_attributes = {}
        if alexa_event.session is not None:
            session_attributes = alexa_event.session.attributes
            
        response_package = ResponsePackage(alexa_response._response, session_attributes)
        return self._encode_response(response_package)

    def _encode_response(self, response_package):
        '''
        Process the response package back to a data type to be sent to Alexa.
        '''
        return json.dumps(response_package.get_json_data())