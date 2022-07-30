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
label_url = "https://kr-shipmultichannel.s3.ap-southeast-1.amazonaws.com/1387189/labels/1659203322_shipping-label-241420301-89593757153.pdf"


