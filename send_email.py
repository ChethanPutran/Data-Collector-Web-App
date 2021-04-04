from email.mime.text import MIMEText
import smtplib

def sendEmail(email,height):
    from_email = "caarts.tech@gmail.com"
    from_pass = "Rock@jokes_5577"
    to_email = email
    
    subject ='Height Data'
    message='Your height is <strong>%s</strong>.'% height
    
    msg = MIMEText(message,'html')
    msg['Subject']=subject
    msg['From']=from_email
    msg['To']=to_email
    
    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_pass)
    gmail.send_message(msg)
    