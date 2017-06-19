from askalexa.response.data import JsonResponseData, response_property

class ResponsePackage(JsonResponseData):
    '''
    This is the complete response package that is sent back to Alexa with the
    given response and session attributes.
    '''

    def __init__(self, response, session_attributes):
        self._version = '1.0'
        self._response = response
        self._session_attributes = session_attributes

    @response_property('version')
    def version(self):
        return self._version

    @response_property('sessionAttributes')
    def session_attributes(self):
        return self._session_attributes

    @session_attributes.setter
    def session_attributes(self, attributes):
      self._session_attributes = attributes

    @response_property('response')
    def response(self):
        return self._response

    @response.setter
    def response(self, response):
        self._response = response