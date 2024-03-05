import os

from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
caregiver_phone_number = os.getenv('CAREGIVER_PHONE_NUMBER')


def send_mms(body):
    """
    Send an MMS message using Twilio.

    Parameters:
    body (str): The content of the MMS message.

    Returns:
    bool: True if the message was sent successfully, False otherwise.
    """
    message = client.messages \
        .create(
            body=body,
            from_=twilio_phone_number,
            to=caregiver_phone_number
    )

    # The status "queued", "sending", or "sent" can indicate success in
    # Twilio async process
    if message.status in ['queued', 'sending', 'sent']:
        return True
    else:
        return False
