from collections import MutableSequence

class JsonResponseData(object):
    '''
    Base class where all response classes should inherit
    '''

    def get_json_data(self):
        '''
        Recursive function to get JSON data that are
        decorated with a response_property.

        Returns a dictionary
        '''
        json_data = {}

        convert_value = lambda v: v.get_json_data() if \
                                  isinstance(v, JsonResponseData) else v

        cls = self.__class__
        for name in dir(cls):
            attr = getattr(cls, name)
            if isinstance(attr, response_property):
                value = getattr(self, name)

                if isinstance(value, MutableSequence):
                    value = map(convert_value, value)
                else:
                    value = convert_value(value)

                if value is not None:
                    json_data[attr.parameter] = value

        # perform the validation before returning data
        # we do this after so we get the most nested
        # instance to validate rather than the top most
        self._validate()

        return json_data

    def _validate(self):
        # subclasses should overload this to raise an exception
        # if the data is not valid or exceeds certain limits
        pass

class response_property(object):
    '''
    A class that behaves like a property decorator, but
    allows for a json parameter to be set.
    '''

    def __init__(self, parameter):
        self.parameter = parameter
        self.fget = None
        self.fset = None

    def __call__(self, func):
        self.fget = func
        self.__doc__ = func.__doc__
        return self

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        if self.fget is None:
            raise AttributeError('Unreadable attribute')

        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("Unable to set attribute")

        self.fset(obj, value)

    def setter(self, fset):
        self.fset = fset
        return self