from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.deprecation import MiddlewareMixin
import re

class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to verify JWT token for every request except the ones in the exclusion list.
    """

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()  # Use DRF's JWT Authentication class

        # Define URL patterns to exclude from token verification
        self.excluded_paths = [
            r'^/api/login/$',       # Exclude login endpoint
            r'^/api/register/$',    # Exclude register endpoint
            r'^/api/marketplace/products/.*$',  # Exclude products api
            r'^/api/marketplace/categories/$',  # Exclude categories api
            r'^/admin/.*$',    # Exclude all endpoints under /api/public/
            r'^/media/documents/.*$', 
            r'^/api/marketplace/landing/.*$', 
        ]

    def __call__(self, request):
        # Check if the current request path matches any excluded pattern
        if self.is_excluded_path(request.path):
            return self.get_response(request)

        try:
            # Try to authenticate the request
            auth_result = self.jwt_auth.authenticate(request)

            if auth_result is not None:
                # If authentication is successful, add the user to the request
                request.user, request.auth = auth_result
            else:
                # If no token is provided or authentication fails
                raise AuthenticationFailed("Unauthorized access")

        except AuthenticationFailed:
            return self._unauthorized_response()

        # Proceed with the request
        return self.get_response(request)

    def is_excluded_path(self, path):
        """
        Check if the request path matches any pattern in the excluded paths.
        """
        for pattern in self.excluded_paths:
            if re.match(pattern, path):
                return True
        return False

    def _unauthorized_response(self):
        from django.http import JsonResponse
        return JsonResponse({"detail": "Unauthorized access"}, status=401)
