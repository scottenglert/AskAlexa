'''
Alexa Main Response Module
==========================
'''
from askalexa.response.data import JsonResponseData, response_property
from askalexa.response.audio import AudioDirective

class Response(JsonResponseData):
    '''
    Main response object that is returned to Alexa. It
    contains the output speech, card, directives and other information
    to send to Alexa.
    '''

    def __init__(self, speech=None, card=None, reprompt=None, session_should_end=True, directives=None):
        self._output_speech = speech
        self._card = card
        self._reprompt = reprompt
        self._session_should_end = session_should_end
        if directives is None:
            directives = []
        elif not isinstance(directives, list):
            directives = [directives]
        self._directives = directives

    @property
    def audio_directive(self):
        if self.directives:
            for d in self.directives:
                if isinstance(d, AudioDirective):
                    return d
        return None

    @audio_directive.setter
    def audio_directive(self, audio_directive):
        existing_directive = self.audio_directive
        if existing_directive:
            self.directives.remove(existing_directive)
        self.directives.append(audio_directive)

    @response_property('outputSpeech')
    def output_speech(self):
        '''
        The output speech object for this response
        '''
        return self._output_speech

    @output_speech.setter
    def output_speech(self, speech):
        self._output_speech = speech

    @response_property('card')
    def card(self):
        '''
        The card for this response.
        '''
        return self._card

    @card.setter
    def card(self, card):
        self._card = card

    @response_property('reprompt')
    def reprompt(self):
        '''
        The reprompt speech object for this response if any.
        '''
        return self._reprompt

    @reprompt.setter
    def reprompt(self, reprompt):
        self._reprompt = reprompt

    @response_property('shouldEndSession')
    def session_should_end(self):
        '''
        True/False if the session should end after this response.
        '''
        return self._session_should_end

    @session_should_end.setter
    def session_should_end(self, session_should_end):
        self._session_should_end = session_should_end

    @response_property('directives')
    def directives(self):
        '''
        The directives for this response.
        '''
        return self._directives

    @directives.setter
    def directives(self, directives):
        self._directives = directives

    def _validate(self):
        # make sure we only have one play directive
        if self.directives is not None:
            if len([d for d in self.directives if isinstance(d, AudioDirective)]) > 1:
                raise Exception("Too many audio directives")

