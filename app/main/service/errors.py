from werkzeug.exceptions import MethodNotAllowed

def custom_error_handler(sender, exception, **kwargs):
    # if isinstance(exception, MethodNotAllowed):
    return "UNHANDLED"
