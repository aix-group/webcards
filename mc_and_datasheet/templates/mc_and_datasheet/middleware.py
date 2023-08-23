# middleware.py

from django.contrib.sessions.signals import session_expired
from django.core.exceptions import MiddlewareNotUsed

class SessionExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        session_expired.connect(self.session_expired_handler, weak=False)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def session_expired_handler(self, sender, session_key, request, **kwargs):
        # This method will be called when a session expires
        # You can trigger the delete view here
        # Example: delete(request, id)

        # Replace 'id' with the appropriate value you need for the delete view
        pass  # Your delete view logic here