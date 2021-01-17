"""Helpers/overrides for django-allauth."""

from django.conf import settings

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class OurSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Customised adapter that recognises other authentication mechanisms."""

    def validate_disconnect(self, account, accounts):
        """Validate whether or not the socialaccount account can be safely disconnected.

        Honours other authentication backends, i.e. ignores unusable passwords if LDAP is used.
        """
        if "django_auth_ldap.backend.LDAPBackend" in settings.AUTHENTICATION_BACKENDS:
            # Ignore upstream validation error as we do not need a usable password
            return None

        # Let upstream decide whether we can disconnect or not
        return super().validate_disconnect(account, accounts)
