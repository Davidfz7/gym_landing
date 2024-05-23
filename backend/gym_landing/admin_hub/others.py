import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

