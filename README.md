# Courier selecting ML Model with Shipping Automation

## Aim :
* On Razorpay webhook Trigger, we want AWS lambda + AWS CloudWatch to Schedules execution of script after 30 min
* Build Robust ML Model for Selecting Courier Partner

## Client's Problem Statement:
1. Selecting courier partner is manual, we have to automate that with high performance courier partner ML Model build on previous data.
2. Client don't want his address and contact details should be printed label.
3. Sending edited PDF Label to Printing Executive over Mail so that he can print label and provide it to Packing Team.
4. Sending WhatsApp Notification to Packaging Executive so that he can start packing.
5. Client wants to execute entire Process to happen after 30 minutes from placing order.

## Provided Solution to Client (via this project):
1. Build an ML Model which first….
2. Use of PDF.CO API for Editing PDF Label as per the requirement.
3. By using Google Cloud Gmail API via oAuth 2.0
4. By using Twilio API using Sandbox 2.0
5. Hosted complete project on AWS then after webhook request from Razorpay, Script is scheduled to run after 30 min by using AWS Lambda and AWS CloudWatch.
![sample 3](https://user-images.githubusercontent.com/73196470/182379841-85700feb-09be-41e9-81cd-727d20d8cae5.png)

## Automation using AWS S3, Lambda, EventBridge build on CloudWatch 
<br/>
<p align="center">
  <img src="https://raw.githubusercontent.com/donnemartin/data-science-ipython-notebooks/master/images/aws.png" size=20px>
</p>
<br/>

- Selecting Best courier partner as per the previous performance of the courier partner.
- Shipping Automation
  * Fetching all orders details
  * Filtering order status & storing shipping id
  * Generating AWB for respective courier partner ( assisted by ML Model)
  * Scheduling pickup for earliest date
  * Generating Packing Label
  * Removing shipper address from generated pdf label
  * Download final label
      - Sending Gmail to Printing Team with Label PDF attachment
      - Sending WhatsApp Notification to Packing Team

# Courier Selecting ML Model
<br>
<br>
Work under progress
<br>
<br>
<br>
<br>

## How to Use ?
* Generate All your API Keys and Credentials from API Links provided below
* Replace the credentials within 'app.py' file
* Run 🚀🚀 and Save your Time

'asd'

### Authentication Types:
* G-Cloud oAuth 2.0 : https://developers.google.com/gmail/api/quickstart/python
* Shiprocket API : https://apidocs.shiprocket.in/#8a56b4d6-b418-43cf-be25-ead62532aa18
* PDF.co API : https://apidocs.pdf.co/#pdfco-api-v100
* Twilio API : https://www.twilio.com/docs/conversations/quickstart

<strong> PS: This Automation will save a salary of 1 person 🚀
Approx . (20k/month) 🥳<br>
🥂 Party toh banti hai, boss! 🥂 </strong>
