# mc-freestyle


Sends you an email with attached figures for upcomming dividend volume based on metricsdata file. 
Must update most metricsdata csv

Create: .env file with following content

##SENGRID API

SENDGRID_API_KEY="APIKEY"
SENDER_EMAIL_ADDRESS="SNEDER EMAIL"

## Running
to run the metrics and generate email with figures:
python metrics.py

requirements tab has what needs to be imported but this is also in the py file

## Testing
running tests:
pytest


