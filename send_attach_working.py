from Google import Create_Service
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes


def send_mail_with_attahment(final_url_after_address_removal, shippment_id):
    CLIENT_SECRET_FILE = 'desktop_credentials.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    file_attachments = ['result.pdf']

    emailMsg = '1 Order with Shipment ID'+shippment_id+" "+final_url_after_address_removal

    # create email message
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = 'iiitprep.dispatch@gmail.com'
    mimeMessage['subject'] = '1 New order Printout'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))

    # Attach files
    for attachment in file_attachments:
        content_type, encoding = mimetypes.guess_type(attachment)
        main_type, sub_type = content_type.split('/', 1)
        file_name = os.path.basename(attachment)

        f = open(attachment, 'rb')

        myFile = MIMEBase(main_type, sub_type)
        myFile.set_payload(f.read())
        myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
        encoders.encode_base64(myFile)

        f.close()

        mimeMessage.attach(myFile)

    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(
        userId='me',
        body={'raw': raw_string}).execute()

    print(message)

send_mail_with_attahment("link","125")