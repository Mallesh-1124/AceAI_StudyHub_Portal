from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Session authentication without CSRF enforcement.
    
    This is safe for our use case because:
    - CORS restricts which origins can make requests
    - The API is only accessible from trusted frontend origins
    """
    def enforce_csrf(self, request):
        return  # Skip CSRF check
