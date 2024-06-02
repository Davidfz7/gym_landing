import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
def send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, login, password):
    # Create the container email message.
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(login, password)  # Log in to the SMTP server
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully.")
            server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

#sender_email = "david123.dd212@gmail.com"
#receiver_email = "ahernandez20910@gmail.com"
#subject = "Test Email"
#body = "Aja juanki"
#smtp_server = "smtp.gmail.com"
#smtp_port = 587
#login = "david123.dd212@gmail.com"
#password = "mveq bcxi qvxu fboc"
#send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, login, password)

def signup(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.create(serializer.validated_data)
        user.save() 
        user  = User.objects.get(username = request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user = user)
        return Response({"token": token.key, "user": UserSerializer(instance = user).data}, status= status.HTTP_200_OK)
    return Response("Couldnt create the user:)", status= status.HTTP_400_BAD_REQUEST) 

def login(request, format = None):
   user = get_object_or_404(User, username = request.data['username'])
   if not user.check_password(request.data['password']):
       return Response({"detail": "Not found."}, status= status.HTTP_404_NOT_FOUND)
   token, created = Token.objects.get_or_create(user = user)
   serializer = UserSerializer(instance = user)
   return Response({"token": token.key, "user": serializer.data.get("username")})