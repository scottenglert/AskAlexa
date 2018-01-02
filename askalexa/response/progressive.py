'''
Alexa Progressive Response Module
=================================

Provides the functionality to send Alexa a progressive response while
the real response is being processed. This is useful for giving an update
for request that takes a long time.
'''
import json
import requests
from askalexa.response.data import JsonResponseData, response_property

class ProgressiveResponseBuilder(object):
    '''
    This class provides a simple way to create and send a progressive
    response to Alexa while your skill processes the complete response.
    '''

    def __init__(self, request_event):
        '''
        Create a progressive response builder. You only need to create
        one of these per each request and simply call the send speech
        each time you need to send a response. Initialize with the 
        request event object.
        '''
        self._header = ProgressiveHeader(request_event.request.request_id)
        self._api_endpoint = request_event.context.system.api_endpoint + '/v1/directives'
        self._api_access_token = request_event.context.system.api_access_token

    def send_speech(self, speech):
        '''
        Send a progressive speech to Alexa. Returns True if the speech was
        processed, otherwise returns False which means a failure and was not
        sent to the user.
        '''
        directive = ProgressiveDirective(speech)
        response = ProgressiveResponse(self._header, directive)

        headers = {'Content-Type' : 'application/json',
                   'Authorization' : 'Bearer {0}'.format(self._api_access_token)}
        data = json.dumps(response.get_json_data())

        result = requests.post(self._api_endpoint, headers=headers, data=data)
        return result.status_code == 204

class ProgressiveResponse(JsonResponseData):
    '''
    The body of the progressive response data
    '''

    def __init__(self, header, directive):
        self._header = header
        self._directive = directive

    @response_property('header')
    def header(self):
        return self._header

    @response_property('directive')
    def directive(self):
        return self._directive

class ProgressiveHeader(JsonResponseData):
    '''
    Header data for the progressive response
    '''

    def __init__(self, request_id):
        self._request_id = request_id

    @response_property('requestId')
    def request_id(self):
        return self._request_id

class ProgressiveDirective(JsonResponseData):
    '''
    Directive to use for a progressive response
    '''

    LIMITS = 600

    def __init__(self, speech):
        self._speech = speech

    @response_property('type')
    def type(self):
        return 'VoicePlayer.Speak'

    @response_property('speech')
    def speech(self):
        return self._speech

    def _validate(self):
        speech_size = len(self._speech)
        if speech_size > self.LIMITS:
            raise ResponseSizeError('Speech limit exceeded {0} characters: ' \
                                    '{1}'.format(self.LIMIT, speech_size))