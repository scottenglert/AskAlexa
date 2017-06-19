'''
A session is included for standard request types: LaunchRequest, IntentRequest,
and SessionEndedRequest. Other requests will not have a session and will not
include a session instance.
'''

from askalexa.request.application import Application
from askalexa.request.user import User

class Session(object):
    '''
    The session object provides additional context associated with the request.
    '''
    
    def __init__(self, is_new, session_id, application, attributes, user):
        self._is_new = is_new
        self._session_id = session_id
        self._application = application
        self._attributes = attributes
        self._user = user

    @classmethod
    def create_from_json(cls, session_json):
        is_new = session_json['new']
        session_id = session_json['sessionId']
        application = Application.create_from_json(session_json['application'])
        attributes = session_json.get('attributes', {})
        user = User.create_from_json(session_json['user'])

        return cls(is_new=is_new, session_id=session_id, application=application,
                   attributes=attributes, user=user)

    @property
    def is_new(self):
        '''
        A boolean value indicating whether this is a new session.
        Returns true for a new session or false for an existing session.
        '''
        return self._is_new

    @property
    def session_id(self):
        '''
        A string that represents a unique identifier per a users active session.

        .. note::

            A session ID is consistent for multiple subsequent requests for a user
            and session. If the session ends for a user, then a new unique
            session ID value is provided for subsequent requests for the same user.
        '''
        return self._session_id

    @property
    def application(self):
        '''
        The application object for this skill. This can also be accessed
        through context.system.application when there is no session object.
        '''
        return self._application

    @property
    def user(self):
        '''
        An object that describes the user making the request.
        '''
        return self._user

    @property
    def attributes(self):
        '''
        This is a dictionary containing key value pairs of user defined data
        that can persist across the same session. This is an empty dictionary
        when this is a new session.
        '''
        return self._attributes
