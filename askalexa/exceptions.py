'''
Ask Alexa Exception Module
==========================

Contains exceptions related to this module.
'''
class AskAlexaError(Exception):
	pass

class RequestError(AskAlexaError):
	pass

class UnknownRequestType(RequestError):
	pass

class InvalidResponseError(AskAlexaError):
	pass

class ResponseSizeError(InvalidResponseError):
	pass

class SkillNotFoundError(AskAlexaError):
	pass