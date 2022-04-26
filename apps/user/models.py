import os

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from encryption.fields import EncryptedFileField
from utils.helpers import municipality_admin_name,ward_admin_name,municipality_data_collector_name,ward_data_collector_name

class UserProfile(models.Model):
    GENDER_CHOICES = [("Male", _("Male")), ("Female", _("Female")), ("Other", _("Other"))]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to="user/profile/", null=True, blank=True)
    citizenship_number = models.CharField(max_length=200, null=True, blank=True)
    house_number = models.CharField(max_length=200, null=True, blank=True)
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
    country = models.ForeignKey('core.Country', on_delete=models.CASCADE, null=True, blank=True)
    province = models.ForeignKey(
        'core.Province', related_name="user_roles", on_delete=models.CASCADE, null=True, blank=True
    )
    district = models.ForeignKey(
        'core.District', related_name="user_roles", on_delete=models.CASCADE, null=True, blank=True
    )
    municipality = models.ForeignKey(
        'core.Municipality', related_name="roles", null=True, blank=True, on_delete=models.CASCADE
    )
    ward = models.ForeignKey('core.Ward', related_name="roles", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return u'User: {}\'s role: {}'.format(self.user.__str__(), self.group.__str__())

    def save(self, *args, **kwargs):
        municipality, ward = self.municipality, self.ward
        if ward:
            self.municipality = ward.municipality
        super().save(*args, **kwargs)

        if self.group.name in [
            municipality_admin_name, ward_admin_name,municipality_data_collector_name,ward_data_collector_name
        ]:
            codenames = ['add_asset', 'change_asset', 'delete_asset', 'view_asset', 'share_asset']
            permissions = Permission.objects.filter(codename__in=codenames)
            user = self.user
            for permission in permissions:
                user.user_permissions.add(permission)

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
    document = EncryptedFileField(upload_to=upload_to)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u'user {}\'s document: {}'.format(self.user.__str__(), self.document_type)
