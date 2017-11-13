from askalexa.response.card import Card
from askalexa.response.main import Response
from askalexa.response.speech import OutputSpeech, Reprompt
from askalexa.response.audio import AudioDirective

class ResponseBuilder(object):
    '''
    The response builder makes creating responses easier and requires less
    exposure to the individual response objects. This is all handled and
    managed by the builder.
    '''

    def __init__(self):
        self._response = Response()

    def add_speech(self, message, reprompt_message=None, as_ssml=False):
        '''
        Add an output speech to the response. If just the message is given,
        then it will signal to end the session. If a reprompt message is
        provided, then it will keep the session open and get a user reply.

        :param message: the message for the response.
        :type message: str
        :param reprompt_message: the message for the reprompt.
        :type reprompt_message: str
        :param as_ssml: the message should be interpeted as ssml. Default False
        :type as_ssml: bool
        :returns: self
        '''
        self._response.output_speech = OutputSpeech.create(message=message, as_ssml=as_ssml)
        if reprompt_message:
            self._response.reprompt = Reprompt.create(message=reprompt_message, as_ssml=as_ssml)
            self._response.session_should_end = False

        return self

    def add_simple_card(self, title, content):
        '''
        Add a simple card that contains just a title and content.

        :returns: self
        '''
        self._response.card = Card.create(Card.SIMPLE, title=title, content=content)
        return self

    def add_standard_card(self, title, content, small_img_url, large_img_url=None):
        '''
        Add a standard card that contains a title, content, and an image.

        :returns: self
        '''
        self._response.card = Card.create(Card.STANDARD, title=title, text=content)
        self._response.card.set_image_urls(small_img_url, large_img_url)
        return self

    def add_link_account_card(self):
        '''
        Add a card that will ask to link accounts in the Alexa app.

        :returns: self
        '''
        self._response.card = Card.create(Card.LINK_ACCOUNT)
        return self

    def add_permissions_consent_card(self, read_list=False, write_list=False,
                                     full_address=False, country_postal=False):
        '''
        Add a card that asks the user for permissions to access their data such
        as household lists and location.

        :returns: self
        '''
        self._response.card = Card.create(Card.PERMISSIONS_CONSENT,
                                            read_list=read_list,
                                            write_list=write_list,
                                            full_address=full_address,
                                            country_postal=country_postal)
        return self

    def play_audio(self, stream_url, token, expected_pevious_token, offset_in_milliseconds=0):
        '''
        Play the given audio stream. The default behavior is to enqueue the
        audio to the active audio queue.

        :param stream_url: the url for the audio stream to enqueue
        :param token: the token to associate this audio stream with
        :param expected_pevious_token: the token for the previous audio stream
        :param offset_in_milliseconds: the offset to begin playing the audio at
        :returns: self
        '''
        play_directive = AudioDirective.create(AudioDirective.PLAY)
        stream = play_directive.audio_item.stream
        stream.url = stream_url
        stream.token = token
        stream.expected_pevious_token = expected_pevious_token
        stream.offset_in_milliseconds = offset_in_milliseconds
        self._response.audio_directive = play_directive
        retur self

    def stop_audio(self):
        '''
        Add an audio directive to stop playing the audio.

        :returns: self
        '''
        self._response.audio_directive = AudioDirective.create(AudioDirective.STOP)
        return self

    def clear_audio_queue(self, clear_all=False):
        '''
        Clear the audio queue. There is an argument to either clear the queue
        but not stop the currently playing audio (default), or stop and clear
        all audio streams.

        :returns: self
        '''
        clear_directive = AudioDirective.create(AudioDirective.CLEAR_QUEUE)
        if clear_all:
            clear_directive.clear_all()
        self._response.audio_directive = clear_directive
        return self

    @property
    def card(self):
        '''
        Get the card in this response
        '''
        return self._response.card

    @property
    def output_speech(self):
        '''
        Get the output speech of this response
        '''
        return self._response.output_speech

    @property
    def reprompt(self):
        '''
        Get the reprompt of this response
        '''
        return self._response.reprompt

    @property
    def audio_directive(self):
        '''
        Get the audio directive of this response
        '''
        return self._response.audio_directive