import requests
import json
json_data = {
    'email': 'iiitprep.dispatch@gmail.com',
    'password': 'Vishnu@123',
}
headers = {
  'Content-Type': 'application/json'
}
response = requests.post('https://apiv2.shiprocket.in/v1/external/auth/login', headers=headers, json=json_data)
#print(response.json())
auth_res_dict = response.json()
token = auth_res_dict["token"]


ship_id_list = ['241420301', '241420299']


## Send Indivisual PDF as attachment
url_after_add_removal = [
    "https://pdf-temp-files.s3.us-west-2.amazonaws.com/KA0RHB40DZTLEPSCF6B1YN7K29SKIL6W/result.pdf?X-Amz-Expires=3600&X-Amz-Security-Token=FwoGZXIvYXdzEPT%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDKdP%2Fo%2FmnFGKlhlcQSKCAeBP73C%2FHCaztrFoPtE9eKs4WTddKuKCu5oSkGGRl8a1CskYvl0IevGb52eu%2F7zEN3rvOztM31Fr1K9NZM16rgVlDIvDUmNIKXhxpQ7R%2FpmHMZwxK2KixPBsdLIsy1mk0IRzjXGtUSaK1MvYB7lkC5FUsnZh2go4f72QCFy0i86kC1cohtGXlwYyKGt%2Fk8qpqC6Q4ufYP%2BTjlJEmnjlXN%2F4Z5gcAGBysQBkVFDWnF9Vhyo8%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA4NRRSZPHOWCZ6FFG/20220731/us-west-2/s3/aws4_request&X-Amz-Date=20220731T031736Z&X-Amz-SignedHeaders=host&X-Amz-Signature=81db4e9d4865ae43235b08f6b41bc25e847db514750dc763db21d60624878092",
    "https://pdf-temp-files.s3.us-west-2.amazonaws.com/1KR8E1HB3PWSI8BW5IYP3MJJVCFMMEJ8/result.pdf?X-Amz-Expires=3600&X-Amz-Security-Token=FwoGZXIvYXdzEPP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDCzKBDhTqZz%2FhGxIByKCAVyr26tdFaqpsD1BM0xXYYnfKx7%2FrV%2B%2BXHN0S3a1w69Yn5p0yyN4ejbKO0Z9B7P6XBT5zorbPBApmSY9fcAg6q5rjUA6RJ5ZLXVBPtKy2cePTV0aEulFzoowJPkMNTVfMeAnVCd5SHvtfZH8c2WJIux9AnmrSXd4rRaCoxmAlRC1GqQotbOXlwYyKPVFnJscc%2BRdrqEiUr37DnpZ2tixqsMFyYcbryKwAXJPd9rXZGvEqY4%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA4NRRSZPHAAUEQOBZ/20220731/us-west-2/s3/aws4_request&X-Amz-Date=20220731T031814Z&X-Amz-SignedHeaders=host&X-Amz-Signature=7409acc936ab0a3ccefe00211aec83b9f3489128d618913d67bdd55527cf8579"
]

pdf_link = url_after_add_removal[0];

from Google import Create_Service
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes

CLIENT_SECRET_FILE = 'gmail_tokn.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

#file_attachments = ['<Attachment 1>', '<Attachment 2>', '<Attachment n>']
file_attachments = url_after_add_removal

emailMsg = 'Order Label attached'

# create email message
mimeMessage = MIMEMultipart()
mimeMessage['to'] = 'bhagwat.nitrr@gmail.com'
mimeMessage['subject'] = '1 order'
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

