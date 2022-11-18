import json

from werkzeug.exceptions import HTTPException


def register_error_handler(app):
    if app.config.get('DEBUG') is True:
        app.logger.debug('Skipping error handlers in Debug mode')
        return

    @app.errorhandler(Exception)
    def handle_exception(e):
        # HTTP errors
        if isinstance(e, HTTPException):
            return {'message': e.description}, 400

        # Non-HTTP, exceptions only
        return {'message': str(e)}

    @app.after_request
    def handle_response_error(response):
        """
        catch error response, status code >=400
        """
        response_failed_format = {
            'success': False, 
            'data': [], 
            'message': None,
            'error': None
        }

        if int(response.status_code) == 404:
            response_data = json.loads(response.get_data())
            if 'c_not_found' not in response_data:
                response.set_data(json.dumps({'message': 'Resource not found'}))
            else:
                response.set_data(json.dumps({'message': response_data['c_not_found']}))

        if int(response.status_code) >= 400:
            response_data = json.loads(response.get_data())
            if 'message' in response_data:
                response_failed_format.update({'message': response_data['message']})
            if 'error' in response_data:
                response_failed_format.update({'error': response_data['error']})
            else:
                response_failed_format.pop('error')
            response.set_data(json.dumps(response_failed_format))
        return response