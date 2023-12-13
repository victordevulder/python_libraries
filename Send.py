from email.mime.text import MIMEText
import smtplib
from datetime import datetime
import requests
import configparser

config = configparser.ConfigParser()
config.read('send.ini')

def getDateTimeStr():
    now = datetime.now()
    formatted_now = now.strftime("%d/%m/%Y %H:%M:%S")
    return formatted_now

def email(objet:str, message:str, level:str, destinataire:str):
    msg = MIMEText(str(message))
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

def ntfy(objet,message,level,canal=None):
    level = str(level)
    if level == "1":
        tag = ""
    if level == "2":
        tag = "heavy_check_mark"
    if level == "3":
        tag = "loudspeaker"
    if level == "4":
        tag = "warning"
    if level == "5":
        tag = "rotating_light"
        
    requests.post(
        "https://ntfy.sh/" + config['ntfy']['script_report'],
        data=f"""{message}
{getDateTimeStr()}""".encode('utf-8'),
        headers={
            "Title": objet,
            "Priority": level,
            "Tags": tag
        }
    )