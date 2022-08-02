# Courier selecting ML Model with Shipping Automation

## Aim :
* On Razorpay webhook Trigger, we want AWS lambda + AWS CloudWatch to Schedules execution of script after 30 min
* Build Robust ML Model for Selecting Courier Partner

## AWS Automation

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
5. Hosted complete project on AWS then after webhook request from Razorpay, Script is scheduled to run after 30 min by using AWS Lambda and AWS CloudWatch

### Authentication Types:
G-Cloud oAuth 2.0 :
Shiprocket API 
PDF.co API
Webhook?
Twilio API

