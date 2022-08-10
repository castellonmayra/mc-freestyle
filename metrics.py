from pandas import read_csv
from statistics import mean, median
import os
import csv
import plotly.io as pio
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId

pio.kaleido.scope.default_format = "png"

result_df = read_csv("metricsdata.csv")



#  "https://github.com/castellonmayra/mc-freestyle/blob/main/metricsdata.csv"

print(type(result_df))
#print(result_df)
print(result_df.columns)
print(len(result_df))

print(result_df.head(3))

#####

mv_col = result_df["MARKET VALUE"]
print(mv_col)

print(mv_col.max())



###

from plotly.express import bar

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
            y="Event ID", 
            x="MARKET VALUE",
            orientation="h",
            title="Market Value By EVENT ID", 
            
            # from the docs: "The keys of this dict should correspond to column names, 
            # and the values should correspond to the desired label to be displayed.
            labels={"Event ID": "Event ID", "MARKET VALUE": "Market Value"},
          
            color="MARKET VALUE")
fig2.show()


## create directory if not exists 
if not os.path.exists("images"):
    os.mkdir("images")

# Save image to file
fig1.write_image("images/fig1.png")
fig2.write_image("images/fig2.png")
#################
################

import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import date
import plotly.express as px



load_dotenv()


SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL_ADDRESS")


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



def send_email(subject, html, recipient_address=SENDER_EMAIL_ADDRESS):
    """
    Sends an email with the specified subject and html contents to the specified recipient,

    If recipient is not specified, sends to the admin's sender address by default.
    """
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))
    print("SUBJECT:", subject)
    #print("HTML:", html)
    message = Mail(from_email=SENDER_EMAIL_ADDRESS, to_emails=recipient_address, subject=subject, html_content=html)
    message.attachment = create_attachment("images/fig1.png")
    message.attachment = create_attachment("images/fig2.png")

    try:
        response = client.send(message)
        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        return response
    except Exception as e:
        print("OOPS", type(e), e)
        return None


if __name__ == "__main__":
    subject = "[Daily Volume Briefing] This is a test"
    
    html = ""
    html += f"<h3>Good Morning!</h3>"

    html += "<h4>Today's Date</h4>"

    send_email(subject, html)




