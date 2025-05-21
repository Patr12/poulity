from django.core.mail import send_mail

def send_update_email(subject, message, recipient_email):
    send_mail(
        subject,
        message,
        'msukwafedrick9@gmail.com',  # Sender
        [recipient_email],      # Recipient list
        fail_silently=False,
    )
