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









# Editing PDF
label_pdf_url = "https://kr-shipmultichannel.s3.ap-southeast-1.amazonaws.com/1387189/labels/1659203322_shipping-label-241420301-89593757153.pdf"
import os
import requests # pip install requests

# The authentication key (API Key).
# Get your own by registering at https://app.pdf.co
API_KEY = "iiitprep@gmail.com_2ba9dc5a8c77eff8e5115e096f1eb41b9c03c32197dac0573acd957a5b6acc687d440bdd"

# Base URL for PDF.co Web API requests
BASE_URL = "https://api.pdf.co/v1"

# Direct URL of source PDF file.
# You can also upload your own file into PDF.co and use it as url. Check "Upload File" samples for code snippets: https://github.com/bytescout/pdf-co-api-samples/tree/master/File%20Upload/
SourceFileURL = label_pdf_url
# PDF document password. Leave empty for unprotected documents.
Password = ""
# Destination PDF file name
DestinationFile = ".\\result.pdf"

def main(args = None):
    replaceStringFromPdf(SourceFileURL, DestinationFile)


def replaceStringFromPdf(uploadedFileUrl, destinationFile):
    """Replace Text from PDF using PDF.co Web API"""

    # Prepare requests params as JSON
    # See documentation: https://apidocs.pdf.co
    parameters = {}
    parameters["name"] = os.path.basename(destinationFile)
    parameters["password"] = Password
    parameters["url"] = uploadedFileUrl
    parameters["searchString"] = "Alternate No.: - 8208656844"
    parameters["replaceString"] = ""

    # Prepare URL for 'Replace Text from PDF' API request
    url = "{}/pdf/edit/replace-text".format(BASE_URL)

    # Execute request and get response as JSON
    response = requests.post(url, data=parameters, headers={ "x-api-key": API_KEY })

    if (response.status_code == 200):
        json = response.json()

        if json["error"] == False:
            #  Get URL of result file
            resultFileUrl = json["url"]
            print(resultFileUrl)
            # Download result file
            r = requests.get(resultFileUrl, stream=True)
            if (r.status_code == 200):
                with open(destinationFile, 'wb') as file:
                    for chunk in r:
                        file.write(chunk)
                print(f"Result file saved as \"{destinationFile}\" file.")
            else:
                print(f"Request error: {response.status_code} {response.reason}")
        else:
            # Show service reported error
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")

if __name__ == '__main__':
    main()