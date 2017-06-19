from askalexa.request.system import System
from askalexa.request.audio import CurrentPlaybackState

class Context(object):
    '''
    The context object provides your skill with information about the current
    state of the Alexa service and device at the time the request is sent to
    your service. This is included on all requests. For requests sent in the
    context of a session (LaunchRequest and IntentRequest), the context object
    duplicates the user and application information that is also available in
    the session.
    '''

    def __init__(self, system, audio_player=None):
        self._system = system
        self._audio_player = audio_player

    @classmethod
    def create_from_json(cls, context_json):
        system = System.create_from_json(context_json['System'])
        audio_player_json = context_json.get('AudioPlayer')

        audio_player = None
        if audio_player_json:
            audio_player = CurrentPlaybackState.create_from_json(audio_player_json)

        return cls(system=system, audio_player=audio_player)

    @property
    def system(self):
        return self._system

    @property
    def audio_player(self):
        return self._audio_player