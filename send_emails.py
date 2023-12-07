import os
import smtplib
# For guessing MIME type based on file name extension
import mimetypes
import time

from email.message import EmailMessage

from message import get_email
from gmail import gmail_send_message


def santa_emails(partecipants, path, subject):
    sender = input("Username: ")

    def generate_emails(table_row):
        i, (receiver, name) = table_row
        zipf = os.path.join(path, name + ".zip")
        email = prepare_email(sender, receiver, subject, zipf)
        return email
    emails = list(map(generate_emails, partecipants.iterrows()))
    send_emails(emails)


def prepare_email(sender, receiver, subject, zipf):
    # Create the message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['To'] = receiver
    msg['From'] = sender
    msg.set_content(get_email())
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    directory, filename = os.path.split(zipf)
    ctype, encoding = mimetypes.guess_type(zipf)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    with open(zipf, 'rb') as fp:
        msg.add_attachment(fp.read(),
                           maintype=maintype,
                           subtype=subtype,
                           filename=filename)
    return msg


# def send_emails(sender, emails):
#     password = getpass("Token: ")
#     url = 'smtp.gmail.com'
#     port = 587
#     server = smtplib.SMTP(url, port)
#     # server.ehlo()
#     server.starttls()
#     # server.ehlo()
#     server.login(sender, password)
#     for email in emails:
#         server.send_message(email)
#     server.quit()

def send_emails(emails):
    num_emails = len(emails)
    for i, email in enumerate(emails):
        gmail_send_message(email)
        time.sleep(1)
        print(f"Sent {i+1}/{num_emails} emails")
