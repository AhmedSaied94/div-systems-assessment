from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID)

# create send sms function


def send_sms(phone):
    try:
        # create message
        ver = verify.verifications.create(to=phone, channel='sms')
    except TwilioRestException as e:
        return False
    # update message status to canceled for tests
    verify.verifications(ver.sid).update(status='canceled')
    return True
