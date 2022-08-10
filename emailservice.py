
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import date


load_dotenv()


SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL_ADDRESS")


def send_email(subject="[Daily Volume] This is a test", html="<p>Hello World</p>", recipient_address=SENDER_EMAIL_ADDRESS):
    """
    Sends an email with the specified subject and html contents to the specified recipient,

    If recipient is not specified, sends to the admin's sender address by default.
    """
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))
    print("SUBJECT:", subject)
    #print("HTML:", html)

    message = Mail(from_email=SENDER_EMAIL_ADDRESS, to_emails=recipient_address, subject=subject, html_content=html)
    try:
        response = client.send(message)
        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        return response
    except Exception as e:
        print("OOPS", type(e), e)
        return None

todays_date = date.today().strftime('%A, %B %d, %Y')

if __name__ == "__main__":
    subject = "[Daily Volume Briefing] This is a test"
    
    html = ""
    html += f"<h3>Good Morning!</h3>"

    html += "<h4>Today's Date</h4>"
    html += f"<p>{todays_date}</p>"

    html += f"<h4>Weather Forecast for {fig1.show()}</h4>"
    html += "<ul>"
    for forecast in result["hourly_forecasts"]:
        html += f"<li>{forecast['timestamp']} | {forecast['temp']} | {forecast['conditions'].upper()}</li>"
    html += "</ul>"

    send_email(subject, html)
