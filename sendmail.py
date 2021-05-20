
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
EMAIL="getbinancemail@gmail.com"
PASS="Hello123!"

def sendMail():
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL,PASS)
        
        msg = EmailMessage()
        msg["From"] = EMAIL
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        msg["Subject"] = current_time+" with 1 hour"
        msg["To"] = "danigalacticu8@hotmail.com"
        msg.set_content("This is the message body")
        msg.add_attachment(open("longgrowings.txt", "r").read(), filename="longgrowings.txt")
    
        smtp.send_message(msg)
    
def main():
    i=1
    while(True):
        if(i>0):
            sendMail()
            time.sleep(60)

main()