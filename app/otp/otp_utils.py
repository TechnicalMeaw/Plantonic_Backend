
import os
import requests
from ..config import settings
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

def send_sms_otp(otp: int, phone: str):
    res = requests.get(f'{settings.sms_otp_base_url}?authorization={settings.sms_otp_auth_key}&route=otp&variables_values={otp}&flash=0&numbers={phone}').json()
    return res['return'] == True

def send_voice_otp(otp: int, phone: str):
    res = requests.get(f'{settings.voice_otp_base_url}?authorization={settings.sms_otp_auth_key}&route=otp&variables_values={otp}&numbers={phone}').json()
    return res['return'] == True


conf = ConnectionConfig(
    MAIL_USERNAME= settings.otp_mail,
    MAIL_PASSWORD= settings.otp_password,
    MAIL_FROM = settings.otp_mail,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True
)


async def send_email_otp(otp: int, email: str, name: str):

    message = MessageSchema(
        subject="Your One Time Password (OTP) From Plantonic",
        recipients=[email,],  # List of recipients, as many as you can pass  
        body='<!DOCTYPE html>' +
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">' +
            '<head>' +
            '<title></title>' +
            '<meta http-equiv="X-UA-Compatible" content="IE=edge">' +
            '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">' +
            '<meta name="viewport" content="width=device-width, initial-scale=1">' +
            '<style type="text/css">' +
            '#outlook a {' +
            'padding: 0;' +
            '}' +
            'body {' +
            'margin: 0;' +
            'padding: 0;' +
            '-webkit-text-size-adjust: 100%;' +
            '-ms-text-size-adjust: 100%;' +
            '}' +
            'table,' +
            'td {' +
            'border-collapse: collapse;' +
            'mso-table-lspace: 0pt;' +
            'mso-table-rspace: 0pt;' +
            '}' +
            'img {' +
            'border: 0;' +
            'height: auto;' +
            'line-height: 100%;' +
            'outline: none;' +
            'text-decoration: none;' +
            '-ms-interpolation-mode: bicubic;' +
            '}' +
            'p {' +
            'display: block;' +
            'margin: 13px 0;' +
            '}' +
            '</style>' +
            '<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,500,700" rel="stylesheet" type="text/css">' +
            '<style type="text/css">' +
            '@import url(https://fonts.googleapis.com/css?family=Open+Sans:300,400,500,700);' +
            '</style>' +
            '<!--<![endif]-->' +
            '<style type="text/css">' +
            '@media only screen and (min-width:480px) {' +
            '.mj-column-per-100 {' +
            'width: 100% !important;' +
            'max-width: 100%;' +
            '}' +
            '}' +
            '</style>' +
            '<style media="screen and (min-width:480px)">' +
            '.moz-text-html .mj-column-per-100 {' +
            'width: 100% !important;' +
            'max-width: 100%;' +
            '}' +
            '</style>' +
            '<style type="text/css">' +
            '@media only screen and (max-width:480px) {' +
            'table.mj-full-width-mobile {' +
            'width: 100% !important;' +
            '}' +
            'td.mj-full-width-mobile {' +
            'width: auto !important;' +
            '}' +
            '}' +
            '</style>' +
            '</head>' +
            '<body style="word-spacing:normal;background-color:#ffffff;">' +
            '<div style="background-color:#ffffff;">' +
            '<div style="margin:0px auto;max-width:600px;">' +
            '<table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">' +
            '<tbody>' +
            '<tr>' +
            '<td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:20px;padding-top:20px;text-align:center;">' +
            '<div style="background:#ffffff;background-color:#ffffff;margin:0px auto;max-width:600px;">' +
            '<table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;background-color:#ffffff;width:100%;">' +
            '<tbody>' +
            '<tr>' +
            '<td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:20px;padding-top:20px;text-align:center;">' +
            '<div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">' +
            '<table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:middle;" width="100%">' +
            '<tbody>' +
            '<tr>' +
            '<td align="start" style="font-size:0px;padding:10px 25px;padding-right:25px;padding-left:25px;word-break:break-word;">' +
            f'<div style="font-family:open Sans Helvetica, Arial, sans-serif;font-size:16px;line-height:1;text-align:start;color:#000000;"><span>Hello {name},</span></div>' +
            '</td>' +
            '</tr>' +
            '<tr>' +
            '<td align="start" style="font-size:0px;padding:10px 25px;padding-right:25px;padding-left:25px;word-break:break-word;">' +
            '<div style="font-family:open Sans Helvetica, Arial, sans-serif;font-size:16px;line-height:1;text-align:start;color:#000000;">Please use the one time password (OTP) below to authenticate yourself:</div>' +
            '</td>' +
            '</tr>' +
            '<tr>' +
            '<td align="start" style="font-size:0px;padding:10px 25px;word-break:break-word;">' +
            f'<div style="font-family:open Sans Helvetica, Arial, sans-serif;font-size:24px;font-weight:bold;line-height:1;text-align:start;color:#000000;">{otp}</div>' +
            '</td>' +
            '</tr>' +
            '<tr>' +
            '<td align="start" style="font-size:0px;padding:10px 25px;padding-right:16px;padding-left:25px;word-break:break-word;">' +
            '<div style="font-family:open Sans Helvetica, Arial, sans-serif;font-size:16px;line-height:1;text-align:start;color:#000000;">This code will be valid for next 5 minutes only.</div>' +
            '</td>' +
            '</tr>' +
            '<tr>' +
            '<td align="start" style="font-size:0px;padding:10px 25px;padding-right:25px;padding-left:25px;word-break:break-word;">' +
            '<div style="font-family:open Sans Helvetica, Arial, sans-serif;font-size:16px;line-height:1;text-align:start;color:#000000;"><br />Thanks & Regards,<br />Team Plantonic.</div>' +
            '</td>' +
            '</tr>' +
            '</tbody>' +
            '</table>' +
            '</div>' +
            '</td>' +
            '</tr>' +
            '</tbody>' +
            '</table>' +
            '</div>' +
            '</div>' +
            '</body>' +
            '</html>',
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)