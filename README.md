# AskAlexa
AskAlexa is a generic framework for implementing a custom Amazon Alexa Skill. It is intended to work with any web framework such as django, flask, and more.

## Features
* Multiple skills can be handled with a single server.
* Provides request verification needed to pass skill certification.

## Prerequisites
* Python 2.7
* PyOpenSSl
* Requests

## Example

    import askalexa
    
    mySkill = askalexa.Skill('my-app-id')
    
    @mySkill.on_launch
    def welcome_response(request_event):
        response = askalexa.ResponseBuilder()
        respones.add_speech('Welcome to my skill!')
        return response
