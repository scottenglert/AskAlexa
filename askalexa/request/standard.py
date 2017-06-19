'''
Standard Request Types and Intents
'''

from askalexa.request.base import BaseRequest

LAUNCH_REQUEST_TYPE = 'LaunchRequest'
INTENT_REQUEST_TYPE = 'IntentRequest'
SESSION_ENDED_REQUEST_TYPE = 'SessionEndedRequest'

class LaunchRequest(BaseRequest):
    '''
    A LaunchRequest is an object that represents that a user made a request to
    an Alexa skill, but did not provide a specific intent.
    '''

    request_type = LAUNCH_REQUEST_TYPE

class SessionEndedRequest(BaseRequest):
    '''
    A SessionEndedRequest is an object that represents a request made to an
    Alexa skill to notify that a session was ended.
    '''

    request_type = SESSION_ENDED_REQUEST_TYPE

class IntentRequest(BaseRequest):
    '''
    An IntentRequest is an object that represents a request made to a skill
    based on what the user wants to do.
    '''

    request_type = INTENT_REQUEST_TYPE

    def __init__(self, intent, **kwargs):
        super(IntentRequest, self).__init__(**kwargs)

        self._intent = intent

    @classmethod
    def create_from_json(cls, request_json, **kwargs):
        intent = Intent.create_from_json(request_json['intent'])
        return super(IntentRequest, cls).create_from_json(request_json,
                                            intent=intent, **kwargs)

    @property
    def intent(self):
        '''
        An object that represents what the user wants.
        '''
        return self._intent

class Intent(object):
    '''
    A specific intent that is requested by the user from a skill invocation
    '''

    NONE_STATUS = 'NONE'
    CONFIRMED_STATUS = 'CONFIRMED'
    DENIED_STATUS = 'DENIED'

    def __init__(self, name, slots=None, confirmation_status=NONE_STATUS):
        self._name = name
        self._slots = slots or {}
        self._confirmation_status = confirmation_status

    @classmethod
    def create_from_json(cls, intent_json):
        name = intent_json['name']
        slots_json = intent_json.get('slots')
        confirmation_status = intent_json.get('confirmationStatus', cls.NONE_STATUS)
        slots = {}
        if slots_json:
            slots = dict(((name, Slot.create_from_json(slot))
                                   for name, slot in slots_json.items()))

        return cls(name=name, slots=slots, confirmation_status=confirmation_status)

    @property
    def name(self):
        '''
        A string representing the name of the intent.
        '''
        return self._name

    @property
    def slots(self):
        '''
        A map of key-value pairs that further describes what the user meant
        based on a predefined intent schema. The map can be empty.
        '''
        return self._slots

    @property
    def confirmation_status(self):
        '''
        An enumeration indicating whether the user has explicitly confirmed
        or denied the entire intent.
        '''
        return self._confirmation_status

class Slot(object):

    NONE_STATUS = 'NONE'
    CONFIRMED_STATUS = 'CONFIRMED'
    DENIED_STATUS = 'DENIED'

    def __init__(self, name, value=None, confirmation_status=NONE_STATUS):
        self._name = name
        self._value = value
        self._confirmation_status = confirmation_status

    @classmethod
    def create_from_json(cls, slot_json):
        name = slot_json['name']
        value = slot_json.get('value')
        confirmation_status = slot_json.get('confirmationStatus', cls.NONE_STATUS)
        return cls(name=name, value=value, confirmation_status=confirmation_status)

    @property
    def name(self):
        '''
        A string that represents the name of the slot.
        '''
        return self._name

    @property
    def value(self):
        '''
        A string that represents the value of the slot. The value is not
        required.
        '''
        return self._value

    @property
    def confirmation_status(self):
        '''
        An enumeration indicating whether the user has explicitly confirmed
        or denied the value of this slot.
        '''
        return self._confirmation_status
