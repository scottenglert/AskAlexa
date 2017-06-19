'''
Alexa Skill Module
==================
'''

from askalexa.dispatcher import RequestDispatcher
from askalexa.request import standard
from askalexa.response import ResponseBuilder

class Skill(object):
    '''
    Skill object that is used to direct incoming requests to the proper 
    command to respond to the request.
    '''

    def __init__(self, application_id, register=True):
        '''
        Initialize a new skill with the given application ID. The skill will be
        registered to the dispatcher if register is True.
        '''
        self._application_id = application_id

        self._session_started_func = None
        self._failsafe_func = self.default_response
        self._request_funcs = {}
        self._intent_funcs = {}
        
        if register:
            RequestDispatcher.add_skill(self)

    def __hash__(self):
        '''
        The hash of a skill is the hash of the application id
        '''
        return hash(self.application_id)

    @property
    def application_id(self):
        '''
        The application ID for this skill.
        '''
        return self._application_id

    def on_launch(self, func):
        '''
        Decorator that registers a function to be called on a launch request.
        '''
        self._request_funcs[standard.LAUNCH_REQUEST_TYPE] = func
        return func

    def on_session_started(self, func):
        '''
        Registers a function to be called when a new session is started.
        This function should not return anything but allows you to initialize
        the session.
        '''
        self._session_started_func = func
        return func

    def on_session_ended(self, func):
        '''
        Registers a function to be called when the session has ended.
        '''
        self._request_funcs[standard.SESSION_ENDED_REQUEST_TYPE] = func
        return func

    def on_intent(self, *name):
        '''
        Decorator for a function to handle the given intent name(s).
        '''
        def wrapper(func):
            for n in name:
                self._intent_funcs[n] = func
            return func

        return wrapper

    def on_request(self, request_type):
        '''
        Decorator for the function to call for the given request type
        '''
        def wrapper(func):
            self._request_funcs[request_type] = func
            return func

        return wrapper

    def on_failsafe(self, func):
        '''
        If no function matches the request, call this function to provide an
        automatic failsafe response.
        '''
        self._failsafe_func = func
        return func

    def default_response(self, event):
        '''
        This is a default response if no function can handle the request. You
        can override this to provide your own default or use the on_failsafe
        decorator to handle a failed request.
        '''
        response = ResponseBuilder()
        response.add_speech('This skill is unable to respond to this request. Sorry!')
        return response

    def get_response(self, event):
        '''
        Get the skill response from the given request event. This is normally
        called from the request dispatcher.
        '''
        session = event.session

        if session is not None and session.is_new and self._session_started_func is not None:
            # call the session started function if there is one
            self._session_started_func(event)

        request = event.request
        request_type = request.request_type

        # if this is a intent request then call the associated function
        # that matches the intent name if the user added to the skill one.
        if request_type == standard.INTENT_REQUEST_TYPE:
            intent_func = self._intent_funcs.get(request.intent.name)
            if intent_func:
                return intent_func(event)

        # fallback to use the request type instead for other types of requests.
        try:
            request_func = self._request_funcs[request_type]
        except KeyError:
            # used a default message since there is no handler
            request_func = self._failsafe_func

        # different request types get different arguments
        return request_func(event)