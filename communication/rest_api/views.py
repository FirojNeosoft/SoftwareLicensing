from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from twilio.rest import Client


from communication.models import *


class SMSView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """
        SMS
        """
        try:
            sms = SMS.objects.create(mobile=request.POST['mobile'], message=request.POST['message'])
            client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(from_=settings.TWILIO_PHONE_NUMBER, body=request.POST['message'],\
                                             to=request.POST['mobile'])
            sms.status = "Sent"
            sms.save()
            data = {
                "status": 200,
                "msg": "SMS sent successfully."
            }
        except Exception as e:
            data = {
                "status": 500,
                "msg": "SMS failed to sent."
            }
        return Response(data)
