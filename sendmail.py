#172.28.25.5:25

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendNotificationMail_plain():
    fromaddr = '184319@cch.org.tw'
    toaddrs  = 'actechforlife@gmail.com'
    subject = 'CCH-AI Center: Reply Notification'
    content = MIMEText("You have a mail to reply to. Please <a href = '#!'>login</a> to attend to this mail. Thank you",'html')
    message = 'Subject: {}\n\n{}'.format(subject, content)

    server = smtplib.SMTP('172.28.25.5')
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, message)
    server.quit()


def sendNotificationMail():
    From = "184319@cch.org.tw"
    to = "actechforlife@gmail.com"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "CCH-AI Center: Reply Notification"
    msg['From'] = From
    msg['To'] = to

    
    html = """\
    <html>
    <head></head>
    <body>
        <p>
        Hello! name,<br>
        You have a mail to attend to.<br>
        Follow this link to reply. <a href="http://192.168.38.233:9079/welcome/talking">link</a> thank you.
        </p>
    </body>
    </html>
    """

    part2 = MIMEText(html, 'html')

    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('172.28.25.5')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(From, to, msg.as_string())
    s.quit()

if __name__ == '__main__':
    sendNotificationMail()