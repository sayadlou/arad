from uuid import uuid4

from django.db import models


class Message(models.Model):
    checked_type = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    subject = models.CharField(max_length=50, db_column="Subject")
    phone = models.CharField(max_length=15, null=True, blank=True, db_column="Phone Number")
    email = models.EmailField(max_length=50, db_column="Email Address")
    content = models.TextField(null=True, db_column="Content")
    checked = models.CharField(max_length=50, choices=checked_type, db_column="Read", default='No')
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)

    def __str__(self):
        return self.subject
