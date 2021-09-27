from django.db import models


class SmsUser(models.Model):
    email = models.EmailField(max_length=100, unique=False)
    password = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False, blank=True)
    sms_count = models.IntegerField()

    def __str__(self):
        return self.email



class SmsLogModel(models.Model):
    user_id = models.IntegerField(unique=False)
    message = models.CharField(max_length=1000)
    count = models.IntegerField()
    contact_no = models.BigIntegerField()

    def __str__(self):
        return self.user_id