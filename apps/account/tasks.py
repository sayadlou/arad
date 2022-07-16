import logging

from django.conf import settings
from kavenegar import KavenegarAPI, APIException, HTTPException

from config import celery

logger = logging.getLogger(__name__)


@celery.task()
def send_sms(message=""):
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        params = {
            'sender': '0935xxxxxxx',  # optional
            'receptor': '0912xxxxxxx',  # multiple mobile number, split by comma
            'message': 'salam',
        }
        response = api.sms_send(params)
        logger.log(1, response)
    except APIException as e:
        logger.error(e)
    except HTTPException as e:
        logger.error(e)
