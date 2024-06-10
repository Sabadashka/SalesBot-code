import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint
import settings


def send_verification_code(email):
    verification_code = randint(1000, 9999)

    message = MIMEMultipart()
    message["From"] = settings.sender_email
    message["To"] = email
    message["Subject"] = "Код підтвердження"

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Email Template</title>
    </head>

    <body style="background-image:linear-gradient(45deg,rgb(245,252,255),rgb(232,242,246));font-family:'Gotham Pro',Roboto,Tahoma,Arial,sans-serif;margin:0;padding:0">
        <div style="text-align:center;padding-top:72px;padding-bottom:5px">
          <table style="display: inline-block;">
            <tbody>
              <tr style="letter-spacing:4px;font-size:40px">
                <td style="font-weight:bold;color:#3e3e3e;">SALES</td>
                <td style="width:10px"></td>
                <td style="font-weight:100;color:#3e3e3e;">BOT</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div style="width:98%;max-width:800px;margin-left:auto;margin-right:auto;background-color:white;border-radius:16px;padding-top:70px;padding-bottom:70px">
            <div style="text-align:center;margin-top:10px">
              <div style="font-size:22px;color:#3e3e3e">«Підтвердження пошти аккаунта»</div>

              <div style="color:#c4c4c4;font-weight:100;margin-top:32px">Код підтвердження:</div>
              <div style="font-size:22px;color:#3e3e3e">{verification_code}</div>
              <div style="color:#9d9d9d;font-weight:100;margin-top:32px">Якщо даний код не Ви надсилали, то просто проігноруйте його</div>
            </div>
        </div>
        <div style="text-align:center;padding-top:72px;padding-bottom:70px">
      </div>
    </body>

    </html>
    """

    message.attach(MIMEText(html_body, 'html'))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.sender_email, settings.sender_password)
        server.sendmail(settings.sender_email, [email], message.as_string())

    return verification_code
