from django.core.mail import send_mail
from django.template.loader import render_to_string

from aleksis.core.db_settings import mail_settings

mail_out = "{} <{}>".format(mail_settings.mail_out_name,
                            mail_settings.mail_out) if mail_settings.mail_out_name != "" else mail_settings.mail_out


def send_mail_with_template(title, receivers, plain_template, html_template, context={}, mail_out=mail_out):
    msg_plain = render_to_string(plain_template, context)
    msg_html = render_to_string(html_template, context)

    try:
        send_mail(
            title,
            msg_plain,
            mail_out,
            receivers,
            html_message=msg_html,
        )
    except Exception as e:
        print("[EMAIL PROBLEM] ", e)
