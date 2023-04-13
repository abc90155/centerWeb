import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


MAIL_SERVER = '172.28.25.5'

def sendamail(content, From = "D9079@cch.org.tw", to = "D9079@cch.org.tw"):    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "CCH-AI Center: Reply Notification"
    msg['From'] = From
    msg['To'] = to
    
    html = """\
    <html>
    <head></head>
    <body>
        <p>{}</p>
        <p>CCH - AI Center</p>
<pre>
Changhua Christian Hospital
AI Research Center
No. 20, Jianbao Street, 3F
Changhua City, 50060
TEL: 04-723-8595 ext. 8373
</pre>
    </body>
    </html>
    """.format(content)

    mail_body = MIMEText(html, 'html')

    msg.attach(mail_body)

    # Send the message via local SMTP server.
    s = smtplib.SMTP(MAIL_SERVER)

    s.sendmail(From, to, msg.as_string())
    s.quit()

if __name__ == '__main__':
    sendamail(content='My content will go here', From='184319@cch.org.tw', to='184319@cch.org.tw')