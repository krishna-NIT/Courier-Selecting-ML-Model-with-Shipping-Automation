import requests
import json
import time
import datetime
import os
import base64
import mimetypes
from Google import Create_Service
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def connect_shiprocet(ship_api_email, ship_api_password):
    json_data = {
        'email': ship_api_email,
        'password': ship_api_password,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post('https://apiv2.shiprocket.in/v1/external/auth/login', headers=headers, json=json_data)
    # print(response.json())

    auth_res_dict = response.json()

    token = auth_res_dict["token"]
    return token


def fetch_order_details_shiprocket(token):
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
    return ship_id_list

# Generate AWB for Shipment
def generate_awb(token, ship_id_list):
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
        ship_id = ship_id_list[i]
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
def pickup_Schedule(token, ship_id_list):
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

def gen_label(token, ship_id_list):
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
    return lable_url_list


def del_txt(SourceFileURL, DestinationFile, del_string):
    # global SourceFileURL

    for i in del_string:
        next_url = deleteTextFromPdf(SourceFileURL, DestinationFile, i)
        SourceFileURL = next_url

    final_pdf_url = SourceFileURL
    return final_pdf_url
    # print(SourceFileURL)


def deleteTextFromPdf(uploadedFileUrl, destinationFile, del_string):
    """Delete Text from PDF using PDF.co Web API"""
    # The authentication key (API Key).
    # Get your own by registering at https://app.pdf.co
    API_KEY = "Your API Key"

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
    ## Auth Completed

    print(del_string)
    # Prepare requests params as JSON
    # See documentation: https://apidocs.pdf.co
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
                status = checkJobStatus(jobId, BASE_URL,API_KEY)  # Possible statuses: "working", "failed", "aborted", "success".

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


def checkJobStatus(jobId, BASE_URL, API_KEY):
    """Checks server job status"""

    url = f"{BASE_URL}/job/check?jobid={jobId}"

    response = requests.get(url, headers={"x-api-key": API_KEY})
    if (response.status_code == 200):
        json = response.json()
        return json["status"]
    else:
        print(f"Request error: {response.status_code} {response.reason}")

    return None


def send_mail_with_attahment(output_file_name, to_email):
    CLIENT_SECRET_FILE = 'desktop_credentials.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    file_attachments = [output_file_name]

    emailMsg = '1 Order with Label attached'

    # create email message
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = to_email
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





## Send WhatsApp Order Notification
def send_whatsapp_msg(order_count):
    from datetime import date
    TWILIO_ACOUNT_SID = 'Your Twilio SID'
    TWILIO_AUTH_TOKEN = 'Your Twilio Auth Token'

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
    from_whatsapp_number = 'whatsapp:+14155238886'
    # replace this number with your own WhatsApp Messaging number
    to_whatsapp_number = 'whatsapp:+91<10 digit no where you want to send notification>'

    print(str(order_count) + ' order at ' + dt_string)

    client.messages.create(body=str(order_count) + ' order at ' + dt_string,
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)




## Main
def main():
    ship_api_email = 'Your Shiprocket API User Email'
    ship_api_password = 'API User Password'
         
    token = connect_shiprocet(ship_api_email, ship_api_password)

    ship_id_list = fetch_order_details_shiprocket(token)

    generate_awb(token, ship_id_list)

    pickup_Schedule(token,ship_id_list)

    gen_label_url = gen_label(token,ship_id_list)
    del_string = ["A-12, Lane no 4, Dnyaneshwar N",
                  "agar Dabki Road, Old City, AKo",
                  "la",
                  "Akola",
                  "444002",
                  "GSTIN:",
                  "Ako"
                  ]
    url_after_add_removal = []
    output_file_name = 'label_after_add_removal.pdf'
    to_email_id = 'iiitprep.dispatch@gmail.com'

    for label_url_p in gen_label_url:
        f_url_pdf = del_txt(label_url_p, output_file_name, del_string)
        url_after_add_removal.append(f_url_pdf)
        send_mail_with_attahment(output_file_name, to_email_id)

    print("Final PDF Links")
    print(len(url_after_add_removal))
    print(url_after_add_removal)
    send_whatsapp_msg(len(ship_id_list))

if __name__ == '__main__':
    main()



