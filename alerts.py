import smtplib
from email.message import EmailMessage

def alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg.set_content(url)
    msg['subject'] = subject
    msg['to'] = to
    

    user = 'email address'
    msg['from'] = user
    password = 'app password created for your email'

    server = smtplib.SMTP("smtp.email_domain", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

# tests if function runs
if __name__ == '__main__':
    alert("subject", "body", "to")
