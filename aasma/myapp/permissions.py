from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from .models import Token
from datetime import datetime

class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        # Extract the token from the request headers
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise AuthenticationFailed(_('Authentication credentials were not provided.'))

        try:
            # Token is typically in the format 'Token <token_key>', so split it
            token_key = auth_header.split(' ')[1]
        except IndexError:
            raise AuthenticationFailed(_('Invalid token format.'))

        # Retrieve the token document from the MongoDB database using mongoengine
        token = Token.objects(key=token_key).first()

        if not token:
            raise AuthenticationFailed(_('Invalid or expired token.'))

        # Check if the token has expired
        if token.expires_at < datetime.utcnow():
            raise AuthenticationFailed(_('Token has expired.'))

        # Assign the user to the request object
        request.user = token.employee  # Use 'employee' instead of 'user'

        # If the token is valid and not expired, grant access
        return True
