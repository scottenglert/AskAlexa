from askalexa.response.data import JsonResponseData, response_property
from askalexa.exceptions import InvalidResponseError, ResponseSizeError

class AudioDirective(object):
    '''
    This object will create a new audio directive based on the given directive
    type. Valid types are PLAY, STOP, and CLEAR_ENQUEUED.
    '''

    PLAY = 'Play'
    STOP = 'Stop'
    CLEAR_QUEUE = 'ClearQueue'

    @classmethod
    def create(cls, directive_type, **kwargs):
        '''
        Create one of the audio directive types. Valid types are PLAY,
        STOP, and CLEAR_QUEUE
        '''
        if directive_type == cls.PLAY:
            return PlayDirective(**kwargs)
        elif directive_type == cls.STOP:
            return StopDirective(**kwargs)
        elif directive_type == cls.CLEAR_QUEUE:
            return ClearQueueDirective(**kwargs)

        raise ValueError('Invalid audio directive type: {0}'.format(directive_type))

class BaseAudioDirective(JsonResponseData):
    '''
    Base class for audio directives. Audio directives should inherit from
    this class.
    '''

    def __init__(self, directive_type):
        self._directive_type = directive_type

    @response_property('type')
    def directive_type(self):
        '''
        The audio directive type.
        '''
        return 'AudioPlayer.{0}'.format(self._directive_type)

class PlayDirective(BaseAudioDirective):
    '''
    This directive will enqueue an audio stream to play.

    There are three play behaviors; Replace all, replace enqueued, and
    enqueue. Replace all will stop the current playing audio and clear
    the audio queue and play the given audio stream. Replace enqueued
    will continue to play the current audio stream, but will replace the
    enqueued audio streams with this one. The enqueue behavior will append
    this audio stream to the current list of queued audio streams.
    '''

    REPLACE_ALL = 'REPLACE_ALL'
    ENQUEUE = 'ENQUEUE'
    REPLACE_ENQUEUED = 'REPLACE_ENQUEUED'

    def __init__(self, play_behavior=ENQUEUE):
        '''
        Create a new audio directive. The default play behavior is to enqueue
        the audio item to the current list of audio items.
        '''
        super(PlayDirective, self).__init__(AudioDirective.PLAY)

        self._play_behavior = play_behavior
        self._audio_item = AudioItem()

    def replace_all(self):
        self._play_behavior = self.REPLACE_ALL

    def enqueue(self):
        self._play_behavior = self.ENQUEUE

    def replace_enqueued(self):
        self._play_behavior = self.REPLACE_ENQUEUED
    
    @response_property('playBehavior')
    def play_behavior(self):
        return self._play_behavior

    @response_property('audioItem')
    def audio_item(self):
        '''
        The audio item that gets sent to the audio queue.
        '''
        return self._audio_item

    @audio_item.setter
    def audio_item(self, audio_item):
        self._audio_item = audio_item

    def _validate(self):
        prev_token = self.audio_item.stream.expected_pevious_token

        if self.play_behavior == self.ENQUEUE and prev_token is None:
            # ensure that the audio item stream has a previous token set
            raise InvalidResponseError('Play directives with enqueue behavior ' \
                                       ' must provide a previous stream token')

        elif self.play_behavior != self.ENQUEUE and prev_token is not None:
            # we can not have the audio item stream with a previous token on
            # non-enqueue behaviors
            raise InvalidResponseError('Play directive without enqueue behavior ' \
                                       ' must not provide a previous stream token')

class StopDirective(BaseAudioDirective):
    '''
    This directive will stop the playback of the audio stream.
    '''

    def __init__(self):
        super(StopDirective, self).__init__(AudioDirective.STOP)

class ClearQueueDirective(BaseAudioDirective):
    '''
    Clears the audio playback queue. You can set this directive to clear the
    queue without stopping the currently playing stream, or clear the queue
    and stop any currently playing stream.
    '''

    ENQUEUED = 'CLEAR_ENQUEUED'
    ALL = 'CLEAR_ALL'

    def __init__(self, clear_behavior=ENQUEUED):
        super(ClearQueueDirective, self).__init__(AudioDirective.CLEAR_QUEUE)

        self._clear_behavior = clear_behavior

    def clear_enqueued(self):
        '''
        Clears the queue and continues to play the currently playing stream.
        '''
        self._clear_behavior = self.ENQUEUED

    def clear_all(self):
        '''
        Clears the entire playback queue and stops the currently playing
        stream (if applicable).
        '''
        self._clear_behavior = self.ALL

    @response_property('clearBehavior')
    def clear_behavior(self):
        '''
        Get the clear behavior for this directive.
        '''
        return self._clear_behavior

class AudioItem(JsonResponseData):
    '''
    Contains an object providing information about the audio stream to play.
    '''
    
    def __init__(self):
        self._stream = Stream()

    @response_property('stream')
    def stream(self):
        '''
        The object audio stream the item will play.
        '''
        return self._stream

    @stream.setter
    def stream(self, stream):
        self._stream = stream

class Stream(JsonResponseData):
    '''
    An object representing the audio stream to play.
    '''

    TOKEN_LIMIT = 1024
    URL_LIMIT = 8000

    def __init__(self, url='', token='', offset_in_milliseconds=0, expected_pevious_token=None):
        '''
        Initializes the stream to play the audio at the given URL.
        '''
        self._token = token
        self._url = url
        self._offset_in_milliseconds = offset_in_milliseconds
        self._expected_pevious_token = expected_pevious_token

    @response_property('token')
    def token(self):
        '''
        An opaque token that represents the audio stream.
        '''
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @response_property('url')
    def url(self):
        '''
        Identifies the location of audio content at a remote location.
        '''
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @response_property('offsetInMilliseconds')
    def offset_in_milliseconds(self):
        '''
        The timestamp in the stream from which Alexa should begin playback.
        Set to 0 to start playing the stream from the beginning. Set to any
        other value to start playback from that associated point in the stream.
        '''
        return self._offset_in_milliseconds

    @offset_in_milliseconds.setter
    def offset_in_milliseconds(self, offset):
        self._offset_in_milliseconds = offset

    @response_property('expectedPreviousToken')
    def expected_pevious_token(self):
        '''
        This property is required and allowed only when the playBehavior
        is ENQUEUE. This is used to prevent potential race conditions if
        requests to progress through a playlist and change tracks occur at
        the same time.
        '''
        return self._expected_pevious_token

    @expected_pevious_token.setter
    def expected_pevious_token(self, token):
        self._expected_pevious_token = token

    def _validate(self):
        token_size = len(self.token)
        if token_size > self.TOKEN_LIMIT:
            raise ResponseSizeError('Token limit exceeded {0} characters: ' \
                                    '{1}'.format(self.TOKEN_LIMIT, token_size))

        url_size = len(self.url)
        if url_size > self.URL_LIMIT:
            raise ResponseSizeError('Url limit exceeded {0} characters: ' \
                                    '{1}'.format(self.URL_LIMIT, url_size))

        if self.expected_pevious_token is not None:
            token_size = len(self.expected_pevious_token)
            if token_size > self.TOKEN_LIMIT:
                raise ResponseSizeError('Expected previous token limit exceeded {0} ' \
                                        'characters: {1}'.format(self.TOKEN_LIMIT, token_size))
