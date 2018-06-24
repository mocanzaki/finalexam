import smtplib
import sys, traceback

class SMTP:
    def __init__(self):
        self.user = 'zaky.racing@yahoo.com'  
        self.password = 'Zakika1997'
        self.server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)

    def start(self):
        try:
            self.server.ehlo()
            self.server.login(self.user, self.password)
        except:
            print("Something went wrong creating SMTP connection!")
            traceback.print_exc(file=sys.stdout)

    def close(self):
        try:
            self.server.close()
        except:
            pass

    def send_mail(self, dest, subject, message):

        email_text = 'Subject: {}\n\n{}'.format(subject, message)

        try:  
            self.server.sendmail(self.user, dest, email_text)
            return True
        except:  
            return False
