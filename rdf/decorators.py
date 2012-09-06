from functools import wraps

def save_to_session(*get_arguments):

    def function_wrapper(function):

        @wraps(function)
        def wrapper(request, *args, **kwargs):
            for argument in get_arguments:
                try:
                    value = request.GET[argument]
                except KeyError:
                    pass
                else:
                    request.session[argument] = value

            return function(request, *args, **kwargs)

        return wrapper

    return function_wrapper
