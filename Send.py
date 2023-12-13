from email.mime.text import MIMEText
import smtplib
from datetime import datetime
import requests
import configparser

config = configparser.ConfigParser()
config.read('smtp.ini')

def getDateTimeStr():
    now = datetime.now()
    formatted_now = now.strftime("%d/%m/%Y %H:%M:%S")
    return formatted_now

def email(objet:str, message:str, level:str, destinataire:str):
    msg = MIMEText(message)
    msg['Subject'] = objet
    msg['From'] = config['smtp']['email']
    msg['To'] = destinataire
    mailserver = smtplib.SMTP(config['smtp']['host'], config['smtp']['port'])
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(config['smtp']['email'], config['smtp']['password'])
    mailserver.send_message(msg)
    mailserver.quit()

def ntfy(objet:str,message:str,level:str,canal:str):
    #
    if level == "1":
        tagsList = ""
    elif level == "2":
        tagsList = "heavy_check_mark"
    elif level == "3":
        tagsList = "loudspeaker"
    elif level == "4":
        tagsList = "warning"
    elif level == "5":
        tagsList = "rotating_light"
    requests.post(
        canal,
        data=f"""{message}
{getDateTimeStr()}""".encode('utf-8'),
        headers={
            "Title": objet,
            "Priority": level,
            "Tags": tagsList
        }
    )