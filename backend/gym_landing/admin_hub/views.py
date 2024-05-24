from django.shortcuts import render
from django.http                  import Http404
from django.contrib.auth.models import User
#----------------------------------------------
from rest_framework.parsers     import JSONParser
from rest_framework             import status
from rest_framework.response    import Response
from rest_framework.views       import APIView
from rest_framework.parsers     import FormParser, MultiPartParser, JSONParser 
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
#----------------------------------------------
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .others import send_email, signup, login
class UserView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        path = request.path
        print(path)
        if "/signup/" == path:
            return signup(request)
        if "/login/" == path:
            return login(request)
        return Response("Hello from UserView", status= status.HTTP_200_OK)
    
class AuthView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes =  [IsAuthenticated]
    def get(self, request, format=None):
        print(f'Request auth: {request.auth}')
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
