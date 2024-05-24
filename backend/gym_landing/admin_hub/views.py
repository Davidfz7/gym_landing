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
from .others import send_email
class UserView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        path = request.path
        print(path)
        if "/signup/" == path:
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                user = serializer.create(serializer.validated_data)
                user.save() 
                user  = User.objects.get(username = request.data['username'])
                user.set_password(request.data['password'])
                user.save()
                token = Token.objects.create(user = user)
                return Response({"token": token.key, "user": UserSerializer(instance = user).data}, status= status.HTTP_200_OK)
            return Response("Trying to access the signup view", status = status.HTTP_200_OK)
        if "/login/" == path:
            sender_email = "david123.dd212@gmail.com"
            receiver_email = "ahernandez20910@gmail.com"
            subject = "Test Email"
            body = "Aja juanki"
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            login = "david123.dd212@gmail.com"
            password = "mveq bcxi qvxu fboc"
            send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, login, password)
            return Response("Trying to access the login view", status = status.HTTP_200_OK)
        return Response("Hello from TestView", status= status.HTTP_200_OK)
    
class AuthView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes =  [IsAuthenticated]
    def get(self, request, format=None):
        content = {
            'user': str(request.data),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)