import json
import requests
import os
import time
import datetime
from Google import Create_Service
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes

from app import BASE_URL
from script import CLIENT_SECRET_FILE


def lambda_handler(event, context, json=None):
    json_data = {
        'email': 'Your Shiprocket API User Email',
        'password': 'Shiprocket API User Password',
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post('https://apiv2.shiprocket.in/v1/external/auth/login', headers=headers, json=json_data)
    # print(response.json())

    auth_res_dict = response.json()

    token = auth_res_dict["token"]

    # Sending Mail with Attachments


    ## Fetching Order Details

    url = "https://apiv2.shiprocket.in/v1/external/orders"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    all_order = response.json()

    print(type(all_order.get('data')))
    # print(all_order.get("data")[1].get("status"))
    # print(all_order.get("data")[1].get("shipments")[0].get("id"))
    ls = all_order.get("data")
    # print(len(ls))
    ship_id_list = []
    i = 0;
    while i < len(ls):
        stat = all_order.get("data")[i].get("status")
    ship_id = all_order.get("data")[i].get("shipments")[0].get("id")
    if (stat == "NEW"):
        ship_id_list.append(ship_id)
    i += 1

    print(len(ship_id_list))
    print("Krishna Shippig ID list")
    print(ship_id_list)

    # Generate AWB for Shipment
    url = "https://apiv2.shiprocket.in/v1/external/courier/assign/awb"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    courier_id = "1"  ## for Bluedart
    courier_id2 = "10"  ## for Delhivery
    courier_id3 = "48"  ## for Ekart

    awb_generated = []
    failed_shipping_id = []
    i = 0
    while i < len(ship_id_list):
        payload = json.dumps({
            "shipment_id": ship_id_list[i],
            "courier_id": "1"
        })

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    res = response.json()
    awb_status = res.get("awb_assign_status")
    if awb_status == 1:
        awb = res.get("response").get("data").get("awb_code")
        print("AWB Generated is" + awb)
        awb_generated.append(awb)
    else:
        payload = json.dumps({
            "shipment_id": ship_id_list[i],
            "courier_id": "10"
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        res = response.json()
        awb_status = res.get("awb_assign_status")
        if awb_status == 1:
            awb = res.get("response").get("data").get("awb_code")
            print("AWB Generated is" + awb)
            awb_generated.append(awb)
        else:
            payload = json.dumps({
                "shipment_id": ship_id_list[i],
                "courier_id": "48"
            })

            response = requests.request("POST", url, headers=headers, data=payload)
            # print(response.text)
            res = response.json()
            awb_status = res.get("awb_assign_status")
            if awb_status == 1:
                awb = res.get("response").get("data").get("awb_code")
                print("AWB Generated is" + awb)
                awb_generated.append(awb)
            else:
                failed_shipping_id.append(ship_id)

    i += 1

    print("All Generated AWB")
    print(awb_generated)

    ## Schedule Pickup
    url = "https://apiv2.shiprocket.in/v1/external/courier/generate/pickup"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    for i in ship_id_list:
        list_ship_indiv_id = [i]
    payload = json.dumps({
        "shipment_id": list_ship_indiv_id
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    ## Generate Label
    url = "https://apiv2.shiprocket.in/v1/external/courier/generate/label"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    lable_url_list = []

    for i in ship_id_list:
        list_ship_indiv_id = [i]
    payload = json.dumps({
        "shipment_id": list_ship_indiv_id
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    respo = response.json()
    if respo.get("label_created") == 1:
        lab_url = respo.get("label_url")
        lable_url_list.append(lab_url)

    print("All Label Links Below")
    print(lable_url_list)

    ## Remove Address from PDF

    # The authentication key (API Key).
    # Get your own by registering at https://app.pdf.co
    API_KEY = "API Key"

    # Base URL for PDF.co Web API requests
    BASE_URL = "https://api.pdf.co/v1"

    # Direct URL of source PDF file.
    # SourceFileURL = label_pdf_url
    # PDF document password. Leave empty for unprotected documents.
    Password = ""
    # Destination PDF file name
    DestinationFile = ".\\label_after_add_removal.pdf"
    # (!) Make asynchronous job
    Async = True

    url_after_add_removal = []
    for label_url_p in lable_url_list:
        f_url_pdf = del_txt(label_url_p)
    url_after_add_removal.append(f_url_pdf)
    send_mail_with_attahment()

    print("Final PDF Links")
    print(len(url_after_add_removal))
    print(url_after_add_removal)


def del_txt(SourceFileURL):
    # global SourceFileURL
    del_string = ["A-12, Lane no 4, Dnyaneshwar N",
                  "agar Dabki Road, Old City, AKo",
                  "la",
                  "Akola",
                  "444002",
                  "GSTIN:",
                  "Ako"
                  ]
    for i in del_string:
        next_url = deleteTextFromPdf(SourceFileURL, DestinationFile, i)
        SourceFileURL = next_url

    final_pdf_url = SourceFileURL
    return final_pdf_url

    # print(SourceFileURL)



def checkJobStatus(jobId):
    url = f"{BASE_URL}/job/check?jobid={jobId}"

    response = requests.get(url, headers={"x-api-key": API_KEY})
    if (response.status_code == 200):
        json = response.json()
        return json["status"]
    else:
        print(f"Request error: {response.status_code} {response.reason}")

    return None

    ## Send WhatsApp Order Notification
def send_whatsapp_msg(order_count, ship_id_list):
    TWILIO_ACOUNT_SID = 'Your Twilio SID'
    TWILIO_AUTH_TOKEN = 'Your API Key'

    from twilio.rest import Client

    from datetime import datetime
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    # print("date and time =", dt_string)

    # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
    # client = Client()
    client = Client(TWILIO_ACOUNT_SID, TWILIO_AUTH_TOKEN)
    # this is the Twilio sandbox testing number
    from_whatsapp_number = 'whatsapp:<Your Twilio Numeber>'
    # replace this number with your own WhatsApp Messaging number
    to_whatsapp_number = 'whatsapp:+91<10 digit number where you want to send Notification>'

    print(str(order_count) + ' order at ' + dt_string)

    client.messages.create(body=str(order_count) + ' order at ' + dt_string,
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)
    send_whatsapp_msg(len(ship_id_list), ship_id_list)

    ## Send PDF as Attachment via Email

def deleteTextFromPdf(uploadedFileUrl, destinationFile, del_string):
        print(del_string)
        parameters = {}
        parameters["async"] = Async
        parameters["name"] = os.path.basename(destinationFile)
        parameters["password"] = Password
        parameters["url"] = uploadedFileUrl
        parameters["searchString"] = del_string

        # Prepare URL for 'Delete Text from PDF' API request
        url = "{}/pdf/edit/delete-text".format(BASE_URL)

        # Execute request and get response as JSON
        response = requests.post(url, data=parameters, headers={"x-api-key": API_KEY})
        if (response.status_code == 200):
            json = response.json()
            result_url_our = json.get('url')

            if json["error"] == False:
                # Asynchronous job ID
                jobId = json["jobId"]
                #  URL of the result file
                resultFileUrl = json["url"]

                # Check the job status in a loop.
                # If you don't want to pause the main thread you can rework the code
                # to use a separate thread for the status checking and completion.
                while True:
                    status = checkJobStatus(jobId)  # Possible statuses: "working", "failed", "aborted", "success".

                    # Display timestamp and status (for demo purposes)
                    print(datetime.datetime.now().strftime("%H:%M.%S") + ": " + status)

                    if status == "success":
                        # Download result file
                        r = requests.get(resultFileUrl, stream=True)
                        if (r.status_code == 200):
                            with open(destinationFile, 'wb') as file:
                                for chunk in r:
                                    file.write(chunk)
                            print(f"Result file saved as \"{destinationFile}\" file.")
                        else:
                            print(f"Request error: {response.status_code} {response.reason}")
                        break
                    elif status == "working":
                        # Pause for a few seconds
                        time.sleep(3)
                    else:
                        print(status)
                        break
            else:
                # Show service reported error
                print(json["message"])
        else:
            print(f"Request error: {response.status_code} {response.reason}")
        return result_url_our


def send_mail_with_attahment():
    CLIENT_SECRET_FILE = 'desktop_credentials.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    file_attachments = ['label_after_add_removal.pdf']

    emailMsg = '1 Order with Label attached'

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
