from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

from utils.deployment_backends.kc_access.shadow_models import KobocatUser, KobocatToken
from utils.deployment_backends.kc_access.utils import grant_kc_model_level_perms


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_kobocat_user(sender, instance, created, raw, **kwargs):
    """
        Sync auth_user table between KPI and KC, and, if the user is newly created,
        grant all KoBoCAT model-level permissions for the content types listed in
        `settings.KOBOCAT_DEFAULT_PERMISSION_CONTENT_TYPES`

        this is triggered when we  create  a  user on  our  digitalprofile  main project
        it  creates a kobocat  user which is necessary for  sharing  koboforms and adding submissions
        this  users  can be found in kc.qbitsx.com/admin/auth/user
        this signal started  working  when i returned it in apps.py
    """
    if not settings.TESTING:
        KobocatUser.sync(instance)

        if created:
            # FIXME: If this fails, the next attempt results in
            #   IntegrityError: duplicate key value violates unique constraint
            #   "auth_user_username_key"
            # and decorating this function with `transaction.atomic` doesn't
            # seem to help. We should roll back the KC user creation if
            # assigning model-level permissions fails
            grant_kc_model_level_perms(instance)


@receiver(post_save, sender=Token)
def save_kobocat_token(sender, instance, **kwargs):
    """
    Sync AuthToken table between KPI and KC
    """

    if not settings.TESTING:
        KobocatToken.sync(instance)


@receiver(post_delete, sender=Token)
def delete_kobocat_token(sender, instance, **kwargs):
    """
    Delete corresponding record from KC AuthToken table
    """
    if not settings.TESTING:
        try:
            KobocatToken.objects.get(pk=instance.pk).delete()
        except KobocatToken.DoesNotExist:
            pass
