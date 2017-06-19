from askalexa.request.register import RequestRegister
from askalexa.request.session import Session
from askalexa.request.context import Context

class AlexaEvent(object):
    '''
    This is an request event that received from Alexa containing information
    about what the user is requesting and associated data.
    '''

    def __init__(self, request, version, context=None, session=None):
        self._request = request
        self._context = context
        self._version = version
        self._session = session

    @classmethod
    def create_from_json(cls, request_json):
        # required
        version = request_json['version']
        request = RequestRegister.create_from_json(request_json['request'])

        # optional
        session = None
        session_json = request_json.get('session')
        if session_json:
            session = Session.create_from_json(session_json)

        context = None
        context_json = request_json.get('context')
        if context_json:
            context = Context.create_from_json(context_json)

        return cls(request=request, context=context, version=version, session=session)

    @property
    def request(self):
        '''
        A request object that provides the details of the users request.
        '''
        return self._request

    @property
    def context(self):
        '''
        The context object provides your skill with information about the
        current state of the Alexa service and device at the time the
        request is sent to your service.
        '''
        return self._context

    @property
    def session(self):
        '''
        The session object provides additional context associated with the
        request.
        '''
        return self._session

    @property
    def version(self):
        '''
        The version specifier for the request.
        '''
        return self._version
        