from django.utils.translation import ugettext_lazy as _

import dbsettings


class ThemeSettings(dbsettings.Group):
    colour_primary = dbsettings.StringValue(_("Primary colour"), default="#007bff")
    colour_secondary = dbsettings.StringValue(_("Secondary colour"), default="#007bff")


class MailSettings(dbsettings.Group):
    mail_out_name = dbsettings.StringValue(_("Mail out name"), default="AlekSIS", required=False)
    mail_out = dbsettings.StringValue(_("Mail out address"), default="no-reply@aleksis.org")


class FooterSettings(dbsettings.Group):
    privacy_url = dbsettings.StringValue(_("Link to privacy policy"), default="")
    impress_url = dbsettings.StringValue(_("Link to impress"), default="")


theme_settings = ThemeSettings(_("Global theme settings"))
mail_settings = MailSettings(_("Mail settings"))
footer_settings = FooterSettings(_("Footer links"))

db_settings = {
    "theme": theme_settings,
    "mail": mail_settings,
    "footer": footer_settings
}
