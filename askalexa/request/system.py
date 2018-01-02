from askalexa.request.application import Application
from askalexa.request.user import User
from askalexa.request.device import Device

class System(object):
    '''
    A system object that provides information about the current state of the
    Alexa service and the device interacting with your skill.
    '''

    def __init__(self, application, user, device, api_endpoint, api_access_token):
        self._application = application
        self._user = user
        self._device = device
        self._api_endpoint = api_endpoint
        self._api_access_token = api_access_token

    @classmethod
    def create_from_json(cls, system_json):
        application = Application.create_from_json(system_json['application'])
        user = User.create_from_json(system_json['user'])
        device = Device.create_from_json(system_json['device'])
        api_endpoint = system_json.get('apiEndpoint')
        api_access_token = system_json.get('apiAccessToken')
        return cls(application=application, user=user, device=device,
                    api_endpoint=api_endpoint, api_access_token=api_access_token)

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
    def api_endpoint(self):
        '''
        An object that references the correct base URI to refer to by region.
        The base URI for US calls for device address data is:
        https://api.amazonalexa.com/. The base URI for UK and DE calls for
        device address data is: https://api.eu.amazonalexa.com
        '''
        return self._api_endpoint

    @property
    def api_access_token(self):
        '''
 
        '''
        return self._api_access_token
