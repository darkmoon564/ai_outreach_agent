import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class EmailSender:
    def __init__(self, user_email, app_password):
        self.user_email = user_email
        self.app_password = app_password

    def send_email(self, to_email, subject, content, attachment=None):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.user_email
            msg["To"] = to_email
            msg["Subject"] = subject

        
            msg.attach(MIMEText(content, "plain"))

            
            if attachment is not None and "bytes" in attachment and "name" in attachment:
                part = MIMEApplication(attachment["bytes"], Name=attachment["name"])
                part["Content-Disposition"] = f'attachment; filename="{attachment['name']}"'
                msg.attach(part)

            
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.user_email, self.app_password)
                server.send_message(msg)

            return True, "Sent"

        except Exception as e:
            return False, str(e)

