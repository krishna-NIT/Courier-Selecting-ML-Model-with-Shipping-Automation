import warnings   
warnings.simplefilter("ignore")
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import time


class sendpdf:
    def __init__(self,sender_email,receiver_email,sender_password,subject,body,filename,address_of_file):
        self.sender_email=sender_email
        self.receiver_email=receiver_email
        self.sender_password=sender_password
        self.subject=subject
        self.body=body
        self.filename=filename
        self.address_of_file=address_of_file
        
        
        
    def email_send(self):
        fromaddr =self.sender_email 
        toaddr = self.receiver_email

 
        msg = MIMEMultipart() 
        msg['From'] = fromaddr 
        msg['To'] = toaddr 
        msg['Subject'] = self.subject
        body = self.body
        msg.attach(MIMEText(body, 'plain')) 
    
    
        filename = self.filename
        attachment = open(f"{self.address_of_file}/{self.filename}.pdf","rb") 
        
        p = MIMEBase('application',  _subtype = 'pdf') 
        p.set_payload((attachment).read()) 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        msg.attach(p) 

        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login(fromaddr,self.sender_password ) 
        text = msg.as_string() 
        s.sendmail(fromaddr, toaddr, text) 
        s.quit() 
       