'''
Response Card Module
====================

Contains all the classes for the cards used in responses for the Alexa app.
'''
from askalexa.response.data import JsonResponseData, response_property
from askalexa.exceptions import ResponseSizeError

class Card(object):
    '''
    Factory class for creating simple, standard, link account, and permissions
    cards.
    '''

    SIMPLE = 'Simple'
    STANDARD = 'Standard'
    LINK_ACCOUNT = 'LinkAccount'
    PERMISSIONS_CONSENT = 'AskForPermissionsConsent'

    @classmethod
    def create(cls, card_type, **kwargs):
        '''
        Create a card of the given type. Valid types are SIMPLE, STANDARD, and
        LINK_ACCOUNT
        '''
        if card_type == cls.SIMPLE:
            return SimpleCard(**kwargs)
        elif card_type == cls.STANDARD:
            return StandardCard(**kwargs)
        elif card_type == cls.LINK_ACCOUNT:
            return LinkAccountCard()
        elif card_type == cls.PERMISSIONS_CONSENT:
            return PermissionsConsentCard(**kwargs)

        raise ValueError('Invalid card type: {0}'.format(card_type))

class BaseCard(JsonResponseData):
    '''
    Base class for all card types.
    '''

    LIMIT = 8000

    def __init__(self, card_type):
        self._card_type = card_type

    def __len__(self):
        return 0

    @response_property('type')
    def card_type(self):
        '''
        This type of card (Simple, Standard, or LinkAccount)
        '''
        return self._card_type

    def _validate(self):
        card_size = len(self)
        if card_size > self.LIMIT:
            raise ResponseSizeError('Card limit exceeded {0} characters: ' \
                                    '{1}'.format(self.LIMIT, card_size))

class PermissionsConsentCard(BaseCard):

    READ_HOUSEHOLD_LIST = 'read::alexa:household:list'
    WRITE_HOUSEHOLD_LIST = 'write::alexa:household:list'
    READ_FULL_ADDRESS = 'read::alexa:device:all:address'
    READ_COUNTRY_POSTAL_CODE = 'read::alexa:device:all:address:country_and_postal_code'

    def __init__(self, read_list=False, write_list=False, full_address=False, country_postal=False):
        super(PermissionsConsentCard, self).__init__(Card.PERMISSIONS_CONSENT)

        self._permissions = []
        if read_list:
            self._permissions.append(self.READ_HOUSEHOLD_LIST)
        if write_list:
            self._permissions.append(self.WRITE_HOUSEHOLD_LIST)
        if full_address:
            self._permissions.append(self.READ_FULL_ADDRESS)
        if country_postal:
            self._permissions.append(self.READ_COUNTRY_POSTAL_CODE)

    @response_property('permissions')
    def permissions(self):
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        self._permissions = permissions

class SimpleCard(BaseCard):
    '''
    Simple card with a title and content
    '''

    def __init__(self, title='', content=''):
        super(SimpleCard, self).__init__(Card.SIMPLE)

        self._title = title
        self._content = content

    def __len__(self):
        return len(self.title) + len(self.content)

    @response_property('title')
    def title(self):
        '''
        The title of the card as a string
        '''
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @response_property('content')
    def content(self):
        '''
        The content of a card as a string
        '''
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

class StandardCard(BaseCard):
    '''
    Standard card with a title, text, and image
    '''

    def __init__(self, title='', text='', image=None):
        super(StandardCard, self).__init__(Card.STANDARD)

        self._title = title
        self._text = text
        self._image = image

    def __len__(self):
        size = len(self.title) + len(self.text)
        if self.image:
            size += len(self.image)
        return size

    @response_property('title')
    def title(self):
        '''
        The title of the card as a string
        '''
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @response_property('text')
    def text(self):
        '''
        The text of the card as a string
        '''
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @response_property('image')
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image

    def set_image_urls(self, small_image_url, large_image_url=None):
        self._image = CardImage(small_image_url, large_image_url)

    def remove_image(self):
        self.image = None

class LinkAccountCard(BaseCard):
    '''
    A card to link accounts
    '''

    def __init__(self):
        super(LinkAccountCard, self).__init__(Card.LINK_ACCOUNT)

class CardImage(JsonResponseData):
    '''
    An image for a response card. Contains URLs to images
    '''

    LIMIT = 2000

    def __init__(self, small_image_url, large_image_url=None):
        '''
        Initialize a card with the given image url's. If no large image url is
        given, then it will use the small image url.
        '''
        self._small_image_url = small_image_url
        self._large_image_url = large_image_url

    def __eq__(self, other):
        if isinstance(other, CardImage):
            return self.small_image_url == other.small_image_url and \
                self.large_image_url == other.large_image_url
        return False

    def __len__(self):
        return len(self.small_image_url) + len(self.large_image_url)

    @response_property('smallImageUrl')
    def small_image_url(self):
        '''
        The small image url to display in the card
        '''
        return self._small_image_url

    @small_image_url.setter
    def small_image_url(self, small_image_url):
        self._small_image_url = small_image_url

    @response_property('largeImageUrl')
    def large_image_url(self):
        '''
        The large image url to display in the card
        '''
        # if there is no large image url, then the small url is returned
        return self._large_image_url if self._large_image_url else self.small_image_url

    @large_image_url.setter
    def large_image_url(self, large_image_url):
        self._large_image_url = large_image_url

    def _validate(self):
        '''
        Neither the small or large image url can exceed the limit
        '''
        urls = dict(Small = self.small_image_url,
                    Large = self.large_image_url)

        for img, url in urls.items():
            url_size = len(url)
            if url_size > self.LIMIT:
                raise ResponseSizeError('{0} image url limit exceeded {1} characters: ' \
                                        '{2}'.format(img, self.LIMIT, url_size))