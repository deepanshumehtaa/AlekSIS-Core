from django.dispatch import receiver
from authlib.integrations.django_client import token_update
  
@receiver(token_update)
def on_token_update(sender, token, refresh_token=None, access_token=None):
    """Auto update oauth token."""
    if refresh_token:
        token = OAuth2Token.find(name=name, refresh_token=refresh_token)
    elif access_token:
        token = OAuth2Token.find(name=name, access_token=access_token)
    else:
        return
  
    # Update old token
    token.access_token = token['access_token']
    token.refresh_token = token.get('refresh_token')
    token.expires_at = token['expires_at']
    token.save()
