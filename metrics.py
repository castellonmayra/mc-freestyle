from pandas import read_csv
import os
import csv
import plotly.io as pio
from plotly.express import line
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId

from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail
from datetime import date
import plotly.express as px

from plotly.express import bar

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL_ADDRESS")

pio.kaleido.scope.default_format = "png"

#################
################

def create_images():
    try:
        result_df = read_csv("metricsdata.csv")
    except Exception as e:
        return False


    mv_col = result_df["MARKET VALUE"]
    print(mv_col.max())

    ###


    fig1 = bar(data_frame=result_df, 
                y="SECURITY", 
                x="MARKET VALUE",
                orientation="h",
                title="Market Value By Security", 
                
                # from the docs: "The keys of this dict should correspond to column names, 
                # and the values should correspond to the desired label to be displayed.
                labels={"SECURITY": "Security", "MARKET VALUE": "Market Value"},
            
                color="MARKET VALUE")
    fig1.show()

    fig2 = bar(data_frame=result_df, 
                y="SECURITY", 
                x="Quantity of Desks",
                orientation="h",
                title="Quantity of Desks by Security", 
                
                # from the docs: "The keys of this dict should correspond to column names, 
                # and the values should correspond to the desired label to be displayed.
                labels={"SECURITY": "Security", "Quantity of Desks": "Quantity of Desks"},
            
                color="Quantity of Desks")
    fig2.show()

    fig3 = px.histogram(data_frame=result_df, 
                y="MARKET VALUE", 
                x="Pay Date", 
                color="Region",
                title="Market Value by Pay Date", 
                barmode="group",
                labels={"MARKET VALUE": "Market Value", "Pay Date": "Pay Date"})
    fig3.update_layout(yaxis_tickprefix = '$', yaxis_tickformat = ',.')
    #print(type(fig))
    fig3.show()


    ## create directory if not exists 
    if not os.path.exists("images"):
        os.mkdir("images")

    # Save image to file
    fig1.write_image("images/fig1.png")
    fig2.write_image("images/fig2.png")
    fig3.write_image("images/fig3.png")
    return True


def create_attachment(name):
    img_filepath = name
    with open(img_filepath, 'rb') as f:
        data = f.read()
        f.close()
    encoded_img = base64.b64encode(data).decode()


    return Attachment(
        file_content = FileContent(encoded_img),
        file_type = FileType(name),
        file_name = FileName(name),
        disposition = Disposition('attachment'),
        content_id = ContentId(name)
    )


def send_failure_email():
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    subject = "Failure: No CSV File for Upcomming Dividend Events"
    html = "No csv. Please contact support."
    message = Mail(from_email=SENDER_EMAIL_ADDRESS, to_emails=SENDER_EMAIL_ADDRESS, subject=subject, html_content=html)

    try:
        response = client.send(message)
        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        return response
    except Exception as e:
        print("OOPS", type(e), e)
        return None


def send_email(subject, html):
    """
    
    """
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))
    print("SUBJECT:", subject)

    message = Mail(from_email=SENDER_EMAIL_ADDRESS, to_emails=SENDER_EMAIL_ADDRESS, subject=subject, html_content=html)
    message.attachment = create_attachment("images/fig1.png")
    message.attachment = create_attachment("images/fig2.png")
    message.attachment = create_attachment("images/fig3.png")

    try:
        response = client.send(message)
        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        return response
    except Exception as e:
        print("OOPS", type(e), e)
        return None


def run_program():
    if not create_images():
        send_failure_email()
        return None

    subject = "Upcomming Dividend Events"
    
    todays_date = date.today().strftime('%A, %B %d, %Y')

    html = ""
    html += "<h3>Good Morning! See attached for upcomming dividends the team will be monitoring.</h3>"
    html += f"<h4>{todays_date}</h4>"

    send_email(subject, html)


if __name__ == "__main__":
    run_program()




