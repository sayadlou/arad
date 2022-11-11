import logging
from typing import List

from django.conf import settings
from kavenegar import KavenegarAPI, APIException, HTTPException

from config import celery

logger = logging.getLogger(__name__)


@celery.task()
def send_sms(message: str, receptor: str):
    try:
        kavenegar_api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        params = {
            'sender': settings.KAVENEGAR_SMS_SENDER_NUMBER,
            'receptor': receptor,  # multiple mobile number, split by comma
            'message': message,
        }
        response = kavenegar_api.sms_send(params)
        logger.log(1, response)
    except APIException as e:
        logger.error(e)
    except HTTPException as e:
        logger.error(e)


def clean_tag(uncleaned_tag):
    cleaned_tag = str(uncleaned_tag)
    cleaned_tag = cleaned_tag.lower()
    cleaned_tag = cleaned_tag.strip()
    return cleaned_tag


def get_filename(filename, request):
    return filename.upper()
