# source https://github.com/sendgrid/sendgrid-python/blob/master/use_cases/send_a_single_email_to_a_single_recipient.md

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime, date
from pytz import timezone

message = Mail(
    from_email=os.environ.get('EOSC_FROM_EMAIL'),
    to_emails=os.environ.get('EOSC_TO_EMAIL'),
    subject=f"EOSC-OpenWeatherMap: {datetime.utcnow()} (UTC)",
    html_content=f"<h1>Latest version of the weather and UV-Index are on GitHub</h1>"
    f"<p>UTC date time: {datetime.utcnow()}</p>"
    f"<p><a href='https://github.com/ALT-F1/OpenWeatherMap/tree/master/output_directory/data/latest' target='_blank'>latest data</a></p>"
)
try:
    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sendgrid_client.send(message)
    print(f"status code: \n{response.status_code}")
    print(f"body: \n{response.body}")
    print(f"headers: \n{response.headers}")
except Exception as e:
    print(e)
