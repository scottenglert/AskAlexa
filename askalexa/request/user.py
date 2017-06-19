class User(object):
    '''
    An object the describes the user making the request
    '''
    
    def __init__(self, user_id, access_token, permissions):
        self._user_id = user_id
        self._permissions = permissions
        self._access_token = access_token

    def __eq__(self, other):
        '''
        Return True/False if the user id's match.
        '''
        if isinstance(other, User):
            return self.user_id == other.user_id

        return self.user_id == other

    @classmethod
    def create_from_json(cls, user_json):
        user_id = user_json['userId']
        access_token = user_json.get('accessToken')

        permissions = None
        permissions_json = user_json.get('permissions')
        if permissions_json:
            permissions = Permissions.create_from_json(permissions_json)

        return cls(user_id=user_id, access_token=access_token, permissions=permissions)

    @property
    def user_id(self):
        '''
        A string that represents a unique identifier for the user who made the
        request. The length of this identifier can vary, but is never more than
        255 characters. The userId is automatically generated when a user
        enables the skill in the Alexa app.

        .. note::

            Disabling and re-enabling a skill generates a new identifier.
        '''
        return self._user_id

    @property
    def permissions(self):
        '''
        Contains a consent token allowing the skill access to information
        that the customer has consented to provide, such as address information.
        '''
        return self._permissions

    @property
    def access_token(self):
        '''
        A token identifying the user in another system. This is only provided
        if the user has successfully linked their account.
        '''
        return self._access_token

class Permissions(object):
    '''
    An object for allowing the skill access to information that the user
    has consented to provide, such as address information.
    '''

    def __init__(self, consent_token):
        self._consent_token = consent_token

    @classmethod
    def create_from_json(cls, permissions_json):
        consent_token = permissions_json['consentToken']
        return cls(consent_token=consent_token)

    @property
    def consent_token(self):
        '''
        A token that gives the skill access to customer information that they
        have consented to.
        '''
        return self._consent_token
