import dbsettings
from django.db import models


class MailSettings(dbsettings.Group):
    mail_rebus = dbsettings.EmailValue("Email address for REBUS")
    mail_feedback = dbsettings.EmailValue("Email address for Feedback")


class Support(models.Model):
    class Meta:
        permissions = (
            ('use_rebus', 'Can use REBUS'),
            ('send_feedback', 'Can send feedback')
        )


mail_settings = MailSettings("Mail adresses")
