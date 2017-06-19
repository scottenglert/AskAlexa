from askalexa.response.data import JsonResponseData, response_property
from askalexa.exceptions import ResponseSizeError

class OutputSpeech(JsonResponseData):
    '''
    Speech response to a skill request
    '''

    LIMITS = 8000
    PLAIN_TEXT_TYPE = 'PlainText'
    SSML_TYPE = 'SSML'

    def __init__(self, speech_type, message):
        self._type = speech_type
        self._text = None
        self._ssml = None

        if speech_type == self.PLAIN_TEXT_TYPE:
            self._text = message
        elif speech_type == self.SSML_TYPE:
            self._ssml = message
        else:
            raise TypeError('Speech type is not valid: {0}'.format(speech_type))

    def __len__(self):
        size = len(self.speech_type)
        if self.text:
            size += len(self.text)

        if self.ssml:
            size += len(self.ssml)

        return size

    def __str__(self):
        return self.text or self.ssml

    @classmethod
    def create(cls, message, as_ssml=False):
        speech_type = cls.SSML_TYPE if as_ssml else cls.PLAIN_TEXT_TYPE
        return cls(speech_type, message)

    @classmethod
    def with_plain_text(cls, message):
        '''
        Create a new speech using plain text.

        :param message: the text of the speech
        :type message: str
        :returns: OutputSpeech instance
        '''
        return cls(cls.PLAIN_TEXT_TYPE, message)

    @classmethod
    def with_ssml(cls, ssml):
        '''
        Create a new speech using SSML
        '''
        return cls(cls.SSML_TYPE, ssml)

    @response_property('text')
    def text(self):
        return self._text

    @response_property('ssml')
    def ssml(self):
        return self._ssml

    @response_property('type')
    def speech_type(self):
        return self._type

    def _validate(self):
        speech_size = len(self)
        if speech_size > self.LIMITS:
            raise ResponseSizeError('Speech limit exceeded {0} characters: ' \
                                    '{1}'.format(self.LIMIT, speech_size))

class Reprompt(JsonResponseData):
    '''
    Reprompt object for a response. This currently contains
    just an output speech for the reprompt.
    '''

    def __init__(self, speech):
        self._output_speech = speech

    @classmethod
    def create(cls, message, as_ssml=False):
        speech = OutputSpeech.create(message=message, as_ssml=as_ssml)
        return cls(speech=speech)

    @response_property('outputSpeech')
    def output_speech(self):
        '''
        The output speech of this reprompt.
        '''
        return self._output_speech

    @output_speech.setter
    def output_speech(self, speech):
        self._output_speech = speech