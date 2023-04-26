from django.core.mail import EmailMessage
class Util:
    #static method help to use this class method without instantiating the class itself
    @staticmethod
    def send_email(data):

        email=EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()   