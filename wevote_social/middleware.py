# wevote_social/middleware.py
# Brought to you by We Vote. Be good.
# -*- coding: UTF-8 -*-

"""Social middleware"""

from django.http import HttpResponse
from wevote_social.facebook import FacebookAPI
# from social_django import exceptions as social_exceptions
# from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
# from social_core.exceptions import SocialAuthBaseException
import wevote_functions.admin

logger = wevote_functions.admin.get_logger(__name__)


class SocialMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        print("SocialMiddleware init response:", get_response) # STEVE STEVE STEVE DONT CHECKIN

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
    # def process_request(self, request):
        if hasattr(request, 'user'):
            if request.user and hasattr(request.user, 'social_auth'):
                social_user = request.user.social_auth.filter(
                    provider='facebook',
                ).first()
                if social_user:
                    request.facebook = FacebookAPI(social_user)

        return response

    def process_exception(request, exception):
        # if hasattr(social_exceptions, exception.__class__.__name__):
        #     if exception.__class__.__name__ == 'AuthAlreadyAssociated':
        #         return HttpResponse("AuthAlreadyAssociated: %s" % exception)
        #     else:
        #         raise exception
        # else:
        error_exception = ""
        print_path = ""
        try:
            error_exception = exception.args[0]
        except Exception as e1:
            pass

        if len(error_exception) == 0:
            try:
                error_exception = exception.message
            except Exception as e2:
                error_exception = "Failure in exception processing in our middleware"
                print("Middleware custom: " + error_exception)

        try:
            print_path = request.path
        except Exception as e2:
            pass

        logger.error('From \'{path}\' caught \'{error}\', type: {error_type}'.format(
            path=print_path, error=error_exception, error_type=type(exception)))
        raise exception
