'''
Audio Player Requests Module
============================

This module contains all the request objects associated with the Audio Player
request types.
'''
from askalexa.request.base import BaseRequest

PLAYBACK_STARTED_REQUEST_TYPE = 'AudioPlayer.PlaybackStarted'
PLAYBACK_FINISHED_REQUEST_TYPE = 'AudioPlayer.PlaybackFinished'
PLAYBACK_STOPPED_REQUEST_TYPE = 'AudioPlayer.PlaybackStopped'
PLAYBACK_FAILED_REQUEST_TYPE = 'AudioPlayer.PlaybackFailed'
PLAYBACK_NEARLY_FINISHED_REQUEST_TYPE = 'AudioPlayer.PlaybackNearlyFinished'
SYSTEM_EXCEPTION_ENCOUNTERED = 'System.ExceptionEncountered'

class BaseAudioPlayerRequest(BaseRequest):
    '''
    Base class for audio player requests
    '''

    def __init__(self, token, **kwargs):
        super(BaseAudioPlayerRequest, self).__init__(**kwargs)

        self._token = token

    @classmethod
    def create_from_json(cls, audio_player_json, **kwargs):
        token = audio_player_json['token']
        return super(BaseAudioPlayerRequest, cls).create_from_json(
                        audio_player_json, token=token, **kwargs)

    @property
    def token(self):
        '''
        An opaque token that represents the audio stream that is currently \
        playing.
        '''
        return self._token

class NormalAudioPlayerRequest(BaseAudioPlayerRequest):
    '''
    Base class for normal audio player requests
    '''

    def __init__(self, offset_in_milliseconds, **kwargs):
        super(NormalAudioPlayerRequest, self).__init__(**kwargs)
        
        self._offset_in_milliseconds = offset_in_milliseconds

    @classmethod
    def create_from_json(cls, audio_player_json, **kwargs):
        offset_in_milliseconds = audio_player_json['offsetInMilliseconds']
        return super(NormalAudioPlayerRequest, cls).create_from_json(
                     audio_player_json, offset_in_milliseconds=offset_in_milliseconds,
                     **kwargs)

    @property
    def offset_in_milliseconds(self):
        '''
        Identifies a tracks offset in milliseconds.
        '''
        return self._offset_in_milliseconds

class PlaybackStartedRequest(NormalAudioPlayerRequest):
    '''
    Sent when Alexa begins playing the audio stream previously sent in a Play
    directive. This lets your skill verify that playback began successfully.
    '''

    request_type = PLAYBACK_STARTED_REQUEST_TYPE

class PlaybackFinishedRequest(NormalAudioPlayerRequest):
    '''
    Sent when the stream Alexa is playing comes to an end on its own.
    '''

    request_type = PLAYBACK_FINISHED_REQUEST_TYPE

class PlaybackStoppedRequest(NormalAudioPlayerRequest):
    '''
    Sent when Alexa stops playing an audio stream in response to a voice
    request or an AudioPlayer directive.
    '''

    request_type = PLAYBACK_STOPPED_REQUEST_TYPE

class PlaybackNearlyFinishedRequest(NormalAudioPlayerRequest):
    '''
    Sent when the currently playing stream is nearly complete and the device
    is ready to receive a new stream.
    '''

    request_type = PLAYBACK_NEARLY_FINISHED_REQUEST_TYPE

class PlaybackFailedRequest(BaseAudioPlayerRequest):
    '''
    Sent when Alexa encounters an error when attempting to play a stream.
    '''

    request_type = PLAYBACK_FAILED_REQUEST_TYPE

    def __init__(self, error, current_playback_state, **kwargs):
        super(PlaybackFailedRequest, self).__init__(**kwargs)

        self._error = error
        self._current_playback_state = current_playback_state

    @classmethod
    def create_from_json(cls, audio_player_json, **kwargs):
        error = PlaybackError.create_from_json(audio_player_json['error'])
        current_playback_state = CurrentPlaybackState.create_from_json(
                                    audio_player_json['currentPlaybackState'])

        return super(PlaybackFailedRequest, cls).create_from_json(audio_player_json,
                     error=error, current_playback_state=current_playback_state, **kwargs)

    @property
    def error(self):
        '''
        Contains an object with error information.
        '''
        return self._error

    @property
    def current_playback_state(self):
        '''
        Contains an object providing details about the playback activity
        occurring at the time of the error.
        '''
        return self._current_playback_state

class PlaybackError(object):

    MEDIA_ERROR_UNKNOWN = 'MEDIA_ERROR_UNKNOWN'
    MEDIA_ERROR_INVALID_REQUEST = 'MEDIA_ERROR_INVALID_REQUEST'
    MEDIA_ERROR_SERVICE_UNAVAILABLE = 'MEDIA_ERROR_SERVICE_UNAVAILABLE'
    MEDIA_ERROR_INTERNAL_SERVER_ERROR = 'MEDIA_ERROR_INTERNAL_SERVER_ERROR'
    MEDIA_ERROR_INTERNAL_DEVICE_ERROR = 'MEDIA_ERROR_INTERNAL_DEVICE_ERROR'

    def __init__(self, error_type, message):
        self._error_type = error_type
        self._message = message

    @classmethod
    def create_from_json(cls, error_json):
        error_type = error_json['type']
        message = error_json['message']
        return cls(error_type=error_type, message=message)

    @property
    def error_type(self):
        '''
        Identifies the specific type of error. The table below provides details
        for each error type.
        '''
        return self._error_type

    @property
    def message(self):
        '''
        A description of the error the device has encountered.
        '''
        return self._message

class CurrentPlaybackState(object):
    '''
    This object provides the current state for the AudioPlayer interface.
    '''

    # playback states
    IDLE = 'IDLE'
    PAUSED = 'PAUSED'
    PLAYING = 'PLAYING'
    BUFFER_UNDERRUN = 'BUFFER_UNDERRUN'
    FINISHED = 'FINISHED'
    STOPPED = 'STOPPED'

    def __init__(self, token, offset_in_milliseconds, player_activity):
        self._token = token
        self._offset_in_milliseconds = offset_in_milliseconds
        self._player_activity = player_activity

    @classmethod
    def create_from_json(cls, state_json):
        token = state_json.get('token')
        offset_in_milliseconds = state_json.get('offsetInMilliseconds')
        player_activity = state_json.get('playerActivity')
        return cls(token=token, offset_in_milliseconds=offset_in_milliseconds,
                   player_activity=player_activity)

    @property
    def token(self):
        '''
        An opaque token that represents the audio stream.
        '''
        return self._token

    @property
    def offset_in_milliseconds(self):
        '''
        Identifies a tracks offset in milliseconds at the time the request was
        sent. This is 0 if the track is at the beginning.
        '''
        return self._offset_in_milliseconds

    @property
    def player_activity(self):
        '''
        Indicates the last known state of audio playback.
        '''
        return self._player_activity

class SystemExceptionEncounteredRequest(BaseRequest):
    '''
    If a response to an audio player request causes an error, your skill is
    sent this request.
    '''

    request_type = SYSTEM_EXCEPTION_ENCOUNTERED

    def __init__(self, error, cause, **kwargs):
        super(SystemExceptionEncounteredRequest, self).__init__(**kwargs)

        self._error = error
        self._cause = cause

    @classmethod
    def create_from_json(cls, exception_json, **kwargs):
        cause = exception_json['cause']
        error = SystemExceptionError.create_from_json(exception_json['error'])
        return super(SystemExceptionEncounteredRequest, cls).create_from_json(
            exception_json, error=error, cause=cause, **kwargs)

    @property
    def error(self):
        return self._error

    @property
    def cause(self):
        return self._cause

class SystemExceptionError(object):
    '''
    Error information for when a system exception happens
    '''

    INVALID_RESPONSE = 'INVALID_RESPONSE'
    DEVICE_COMMUNICATION_ERROR = 'DEVICE_COMMUNICATION_ERROR'
    INTERNAL_ERROR = 'INTERNAL_ERROR'

    def __init__(self, message, error_type):
        self._message = message
        self._error_type = error_type

    @classmethod
    def create_from_json(cls, error_json):
        message = error_json['message']
        error_type = error_json['type']
        return cls(message=message, error_type=error_type)

    @property
    def message(self):
        return self._message

    @property
    def error_type(self):
        return self._error_type