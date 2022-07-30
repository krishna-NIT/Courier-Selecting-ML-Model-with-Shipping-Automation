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





url = "https://apiv2.shiprocket.in/v1/external/orders"

payload={}
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {token}'
}

response = requests.request("GET", url, headers=headers, data=payload)
all_order = response.json()


print(type(all_order.get('data')))
#print(all_order.get("data")[1].get("status"))
#print(all_order.get("data")[1].get("shipments")[0].get("id"))
ls = all_order.get("data")
#print(len(ls))
ship_id_list = []
i = 0;
while i < len(ls):
    stat = all_order.get("data")[i].get("status")
    ship_id = all_order.get("data")[i].get("shipments")[0].get("id")
    if(stat == "NEW"):
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

courier_id = "1" ## for Bluedart
courier_id2 = "10" ## for Delhivery
courier_id3 = "48" ## for Ekart

awb_generated = []
failed_shipping_id = []
i = 0
while i < len(ship_id_list):
    payload = json.dumps({
      "shipment_id": ship_id_list[i],
      "courier_id": "1"
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
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
        #print(response.text)
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
            #print(response.text)
            res = response.json()
            awb_status = res.get("awb_assign_status")
            if awb_status == 1:
                awb = res.get("response").get("data").get("awb_code")
                print("AWB Generated is" + awb)
                awb_generated.append(awb)
            else:
                failed_shipping_id.append(ship_id)

    i+=1

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
    #print(response.text)












