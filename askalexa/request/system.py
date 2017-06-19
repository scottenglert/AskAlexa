from askalexa.request.application import Application
from askalexa.request.user import User
from askalexa.request.device import Device

class System(object):
    '''
    A system object that provides information about the current state of the
    Alexa service and the device interacting with your skill.
    '''

    def __init__(self, application, user, device, api_end_point):
        self._application = application
        self._user = user
        self._device = device
        self._api_end_point = api_end_point

    @classmethod
    def create_from_json(cls, system_json):
        application = Application.create_from_json(system_json['application'])
        user = User.create_from_json(system_json['user'])
        device = Device.create_from_json(system_json['device'])
        api_end_point = system_json.get('apiEndpoint')
        return cls(application=application, user=user, device=device, api_end_point=api_end_point)

    @property
    def application(self):
        '''
        The application object for this skill.
        '''
        return self._application

    @property
    def user(self):
        '''
        An object that describes the user making the request.
        '''
        return self._user

    @property
    def device(self):
        '''
        An object providing information about the device used to send the request.
        '''
        return self._device

    @property
    def api_end_point(self):
        '''
        An object that references the correct base URI to refer to by region.
        The base URI for US calls for device address data is:
        https://api.amazonalexa.com/. The base URI for UK and DE calls for
        device address data is: https://api.eu.amazonalexa.com
        '''
        return self._api_end_point  