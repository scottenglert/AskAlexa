class Application(object):
    '''
    An object describing the application the skill is intended for. This is
    identified by an application id.
    '''

    def __init__(self, application_id):
        '''
        application_id: representing the appliation ID for your skill
        '''
        self._application_id = application_id

    def __eq__(self, other):
        if isinstance(other, Application):
            return self.application_id == other.application_id

        return self.application_id == other

    def __str__(self):
        return self.application_id

    @classmethod
    def create_from_json(cls, application_json):
        return cls(application_json['applicationId'])

    @property
    def application_id(self):
        '''
        The application id for this Alexa application.
        '''
        return self._application_id