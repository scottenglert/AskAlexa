'''
Playback Controller Requests

The PlaybackController interface provides requests to notify your skill when
the user interacts with player controls, such as the buttons on a device or
remote control. Your skill can respond to these requests with AudioPlayer
directives to start and stop playback.
'''

from askalexa.request.base import BaseRequest

#: Playback controller request types
NEXT_COMMAND_REQUEST_TYPE = 'PlaybackController.NextCommandIssued'
PAUSE_COMMAND_REQUEST_TYPE = 'PlaybackController.PauseCommandIssued'
PLAY_COMMAND_REQUEST_TYPE = 'PlaybackController.PlayCommandIssued'
PREVIOUS_COMMAND_REQUEST_TYPE = 'PlaybackController.PreviousCommandIssued'

class PlaybackControllerNextRequest(BaseRequest):
    '''
    Sent when the user uses a "next" button with the intent to skip to the
    next audio item.
    '''

    request_type = NEXT_COMMAND_REQUEST_TYPE

class PlaybackControllerPauseRequest(BaseRequest):
    '''
    Sent when the user uses a "pause" button with the intent to stop playback.
    '''

    request_type = PAUSE_COMMAND_REQUEST_TYPE

class PlaybackControllerPlayRequest(BaseRequest):
    '''
    Sent when the user uses a "play" or "resume" button with the intent to
    start or resume playback.
    '''

    request_type = PLAY_COMMAND_REQUEST_TYPE

class PlaybackControllerPreviousRequest(BaseRequest):
    '''
    Sent when the user uses a "previous" button with the intent to go back
    to the previous audio item.
    '''

    request_type = PREVIOUS_COMMAND_REQUEST_TYPE