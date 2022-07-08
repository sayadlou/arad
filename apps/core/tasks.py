from time import sleep

from celery import shared_task

from config import celery


@celery.task()
def send_email(message=""):
    print("Sending Email to 10K person")
    print(message)
    sleep(10)
    print("Email to 10K person Sent")
