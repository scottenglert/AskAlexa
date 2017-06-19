from askalexa.exceptions import SkillNotFoundError

class RequestDispatcher(object):
    '''
    This class will be used to register your Alexa skill. Incoming requests
    will be dispatched to the appropriate skill based on the application ID.
    '''
    #: registered skills will be stored in this dictionary
    _skills = {}

    @classmethod
    def add_skill(cls, skill):
        '''
        Add a skill to the dispatcher.
        '''
        cls._skills[skill.application_id] = skill

    @classmethod
    def remove_skill(cls, skill):
        '''
        Remove a skill from the dispatcher.
        '''
        cls._skills.pop(skill.application_id, None)

    @classmethod
    def dispatch_request(cls, request_event):
        '''
        Dispatch the request to the appropriate skill.
        '''
        if request_event.session is not None:
            application_id = request_event.session.application.application_id
        else:
            application_id = request_event.context.system.application.application_id

        try:
            skill = cls._skills[application_id]
        except KeyError:
            raise SkillNotFoundError('No skill exists for appplication ID: ' \
                                     '{0}'.format(application_id))

        return skill.get_response(request_event)

    @classmethod
    def list_skills(cls):
        '''
        Return a list of current skills.
        '''
        return cls._skills.values()

    @classmethod
    def clear_skills(cls):
        '''
        Clear all skills from the dispatcher.
        '''
        cls._skills.clear()

    @property
    @classmethod
    def skill_count(cls):
        '''
        Returns the number of skills
        '''
        return len(cls._skills)