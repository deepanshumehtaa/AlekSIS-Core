import os
from uuid import uuid4

from django.template.loader_tags import register
from datetime import datetime

from django.utils import timezone, formats
from ics import Calendar


def path_and_rename(instance, filename):
    upload_to = 'menus'
    ext = filename.split('.')[-1].lower()
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


@register.inclusion_tag("components/msgbox.html")
def msg_box(msg, status="success", icon="info"):
    return {"msg": msg, "status": status, "icon": icon}


import requests


def get_newest_articles(domain, limit=0, author_blacklist=None):
    """
    This function returns the newest articles/posts of a wordpress-site.

    :param domain: The domain to get the newest posts from (for example https://wordpress.com). Don't put a slash (/) at the end!
    :param limit: if 0: all posts will be shown, else nly the certain number
    :param author_blacklist: if the authors id (an integer) is in this list, the article won't be displayed
    :return: a list of the newest posts/articles
    """
    if author_blacklist is None:
        author_blacklist = []

    suffix = "/wp-json/wp/v2/posts"

    url = domain + suffix

    site = requests.get(url)
    data = site.json()

    posts = []
    print(data)
    for post in data:
        if post["author"] not in author_blacklist:
            # Now get the link to the image
            if post["_links"].get("wp:featuredmedia", False):
                media_site = requests.get(post["_links"]["wp:featuredmedia"][0]["href"]).json()
                image_url = media_site["guid"]["rendered"]

                posts.append(
                    {
                        "title": post["title"]["rendered"],
                        "short_text": post["excerpt"]["rendered"],
                        "link": post["link"],
                        "image_url": image_url,
                    }
                )
        if len(posts) >= limit and limit >= 0:
            break

    return posts


CALENDAR_URL = "https://nimbus.katharineum.de/remote.php/dav/public-calendars/owit7yysLB2CYNTq?export"


def get_current_events():
    c = Calendar(requests.get(CALENDAR_URL).text)
    print(c.events)
    e = list(c.timeline)[0]
    print(c.timeline.today())
    i = 0
    events = []
    for event in c.timeline.start_after(timezone.now()):
        if i >= 5:
            break
        i += 1

        begin_date_formatted = formats.date_format(event.begin)
        end_date_formatted = formats.date_format(event.end)
        begin_time_formatted = formats.time_format(event.begin.time())
        end_time_formatted = formats.time_format(event.end.time())
        if event.begin.date() == event.end.date():
            formatted = begin_date_formatted
            if not event.all_day:
                formatted += " " + begin_time_formatted
            if event.begin.time != event.end.time():
                formatted += " – " + end_time_formatted
        else:
            if event.all_day:
                formatted = "{} – {}".format(begin_date_formatted, end_date_formatted)
            else:
                formatted = "{} {} – {} {}".format(begin_date_formatted, begin_time_formatted, end_date_formatted,
                                                   end_time_formatted)
        print(formatted)
        print(formats.date_format(event.begin))
        events.append({
            "name": event.name,
            # "begin": event.begin,
            # "end": event.end,
            "formatted": formatted
        })
        # print(event)
    print(events)
    print("Event '{}' started {}".format(e.name, e.begin.humanize()))
    return events
