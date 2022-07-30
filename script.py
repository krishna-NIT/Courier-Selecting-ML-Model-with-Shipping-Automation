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


ship_id_list = ['241417795', '241417794']


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
