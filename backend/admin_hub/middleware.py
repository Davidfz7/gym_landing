from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

class TokenExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Hola")
        if not self.requires_auth_header(request.path_info):
            return self.get_response(request)

        auth = get_authorization_header(request).split() 
        #if auth and auth[0].lower() == b'token':
        if 1: #Trolling a lil bit
            try:
                token = Token.objects.get(key=auth[1].decode())
                if timezone.now() > token.created + timedelta(hours = 1):  
                    token.delete()
                    return self.token_expired_response() 
            except Token.DoesNotExist:
                return self.invalid_token_response()
        response = self.get_response(request)
        return response

    def requires_auth_header(self, path_info):
        excluded_paths = ['/signup/', '/login/', '/get-product/', '/get-all-products/',
                          '/get-imgs-names/','/media/uploads/']
        return not any(path_info.startswith(path) for path in excluded_paths)
    
    def token_expired_response(self): 
        response = Response({"detail": "Token has expired"}, status = status.HTTP_401_UNAUTHORIZED)  # Diccionario para la respuesta JSON
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response

    def invalid_token_response(self):
        response = Response({"detail": "Invalid token"}, status = status.HTTP_401_UNAUTHORIZED)  # Diccionario para la respuesta JSON
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response