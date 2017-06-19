class Device(object):
    '''
    This is an object that provides information about the device making the
    request.
    '''

    def __init__(self, device_id, supported_interfaces):
        self._device_id = device_id
        self._supported_interfaces = supported_interfaces

    @classmethod
    def create_from_json(cls, device_json):
        device_id = device_json.get('deviceId')
        supported_interfaces = device_json['supportedInterfaces']
        return cls(device_id=device_id, supported_interfaces=supported_interfaces)

    @property
    def device_id(self):
        '''
        A unique identifier of the device making the request
        '''
        return self._device_id

    @property
    def supported_interfaces(self):
        '''
        A dictionary with each interface that the device supports. For example,
        if it includes 'AudioPlayer', then you know that the device supports
        streaming audio using the AudioPlayer interface.
        '''
        return self._supported_interfaces