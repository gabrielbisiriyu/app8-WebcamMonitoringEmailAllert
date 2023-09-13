import smtplib,imghdr
from glob import glob 
import os
from email.message import EmailMessage

def send_email(image_path):
    print("Sending email...")
    password = os.getenv("PASSWORD")
    sender="guyex1996@gmail.com"
    receiver="guyex1996@gmail.com"
    email_message=EmailMessage() 
    email_message["Subject"]= "A new customer showed up"
    email_message.set_content("Hwy, we just saw a new customer") 

    with open(image_path,'rb') as fh:
        content=fh.read()  
    
    email_message.add_attachment(content,maintype="image",subtype=imghdr.what(None,content))   
    gmail=smtplib.SMTP_SSL("smtp.gmail.com")
    gmail.login(sender,password)  
    gmail.sendmail(sender,receiver,email_message.as_string())
    gmail.quit()    
    print("Email sent") 

if __name__=="__main__":
    send_email(image_path="image.png") 


