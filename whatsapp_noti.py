


## Send WhatsApp Order Notification
from datetime import date
TWILIO_ACOUNT_SID='Your SID Key'
TWILIO_AUTH_TOKEN='Your Auth Token'

from twilio.rest import Client

from datetime import datetime
# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M")
print("date and time =", dt_string)

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
#client = Client()
client = Client(TWILIO_ACOUNT_SID, TWILIO_AUTH_TOKEN)
# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:+91<10 digit number onto whom you want to send message>'

client.messages.create(body='1 order at '+dt_string,
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)
