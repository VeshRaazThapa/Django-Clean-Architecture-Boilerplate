import os
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

# from apps.encryption.fields import EncryptedFileField

class UserProfile(models.Model):
    GENDER_CHOICES = [("Male", _("Male")), ("Female", _("Female")), ("Other", _("Other"))]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to="user/profile/", null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Device(models.Model):
    """
        Stores information about user devices for fcm notifications
    """
    device_id = models.CharField(max_length=100, null=True, blank=True)
    registration_id = models.TextField()
    email = models.CharField(max_length=100)


class UserRole(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="roles", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="roles", on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return u'User: {}\'s role: {}'.format(self.user.__str__(), self.group.__str__())

    @staticmethod
    def is_active(user, group):
        return UserRole.objects.filter(user=user, group__name=group, ended_at=None).exists()


def upload_to(instance, filename):
    return os.path.join(
        'user', str(instance.user.username),
        'xls',
        os.path.split(filename)[1])


class UserDocument(models.Model):
    DOCUMENT_TYPES = [("Citizenship", _("Citizenship")), ("Birth Certificate", _("Birth Certificate")), ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="documents", on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    # document = EncryptedFileField(upload_to=upload_to)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u'user {}\'s document: {}'.format(self.user.__str__(), self.document_type)
