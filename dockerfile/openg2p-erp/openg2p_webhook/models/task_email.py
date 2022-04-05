import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPException


def send_mail(assigne_name, receiver_address, link):
    # The mail addresses and password

    sender_address = 'noreply@ibank.financial'
    sender_pass = '@y{@TOPFfI{g'
    # receiver_address = 'ranasinghishan@gmail.com'

    print(assigne_name, sender_address, receiver_address, link)

    mail_content = """From: %s<br>
    To: %s<br>
    Subject: OPENG2P Task<br>

    Your OPENG2P Task is pending.<br>
    Assigned by : <b>%s</b><br>

    Go to link : %s to complete your pending tasks.

    """ % (sender_address, receiver_address, assigne_name, link)

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'OPENG2P Task'

    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html'))
    try:
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('199.250.199.36', 587)
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()

    except SMTPException as e:
        print(e)
