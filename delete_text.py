import os
import requests  # pip install requests
import time
import datetime

# The authentication key (API Key).
# Get your own by registering at https://app.pdf.co
API_KEY = "iiitprep@gmail.com_2ba9dc5a8c77eff8e5115e096f1eb41b9c03c32197dac0573acd957a5b6acc687d440bdd"
label_pdf_url = "https://kr-shipmultichannel.s3.ap-southeast-1.amazonaws.com/1387189/labels/1659203322_shipping-label-241420301-89593757153.pdf"

# Base URL for PDF.co Web API requests
BASE_URL = "https://api.pdf.co/v1"

# Direct URL of source PDF file.
SourceFileURL = label_pdf_url
# PDF document password. Leave empty for unprotected documents.
Password = ""
# Destination PDF file name
DestinationFile = ".\\result.pdf"
# (!) Make asynchronous job
Async = True


def main(args=None):
    f_pdf_url = del_txt()
    print(f_pdf_url)


def del_txt():
    global SourceFileURL
    del_string = ["A-12, Lane no 4, Dnyaneshwar N",
                  "agar Dabki Road, Old City, AKo",
                  "la",
                  "Akola",
                  "444002",
                  "GSTIN:",
                  "Phone No.: 8742881915",
                  "Alternate No.: - 8208656844",
                  "Ako"
                  ]
    for i in del_string:
        next_url = deleteTextFromPdf(SourceFileURL, DestinationFile, i)
        SourceFileURL = next_url

    final_pdf_url = SourceFileURL
    return final_pdf_url
    #print(SourceFileURL)


def deleteTextFromPdf(uploadedFileUrl, destinationFile, del_string):
    """Delete Text from PDF using PDF.co Web API"""
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

def checkJobStatus(jobId):
    """Checks server job status"""

    url = f"{BASE_URL}/job/check?jobid={jobId}"

    response = requests.get(url, headers={"x-api-key": API_KEY})
    if (response.status_code == 200):
        json = response.json()
        return json["status"]
    else:
        print(f"Request error: {response.status_code} {response.reason}")

    return None


if __name__ == '__main__':
    main()