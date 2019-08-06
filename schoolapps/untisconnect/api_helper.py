from django.utils import timezone

from . import models

DB_NAME = 'untis'


#####################
# BASIC DEFINITIONS #
#####################
class Basic(object):
    def __init__(self):
        self.filled = False
        self.id = None

    def create(self, db_obj):
        self.filled = True


def run_using(obj):
    return obj.using(DB_NAME)


def get_term_by_ids(term_id, school_year_id):
    data = run_using(models.Terms.objects).get(term_id=term_id, schoolyear_id=school_year_id)
    # print(data.schoolyear_id)
    return data


########
# TERM #
########
class Term(object):
    def __init__(self):
        self.filled = False
        self.id = None
        self.name = None
        self.school_year_id = None

    def create(self, db_obj):
        self.filled = True
        self.id = db_obj.term_id
        self.name = db_obj.longname
        self.school_year_id = db_obj.schoolyear_id


def get_terms():
    data = run_using(models.Terms.objects).all()
    terms = []
    for item in data:
        term = Term()
        term.create(item)
        terms.append(term)
        # print(term.name)
    return terms


##############
# SCHOOLYEAR #
##############
class SchoolYear(object):
    def __init__(self):
        self.filled = False
        self.id = None
        self.name = None

    def create(self, db_obj):
        self.filled = True
        self.id = db_obj.schoolyear_id
        self.name = db_obj.schoolyearzoned


def get_school_years():
    data = run_using(models.Schoolyear.objects).all()
    years = []
    for item in data:
        year = SchoolYear()
        year.create(item)
        years.append(year)
        # print(term.name)
    return years


################
# HELP METHODS #
################
def clean_array(a, conv=None):
    b = []
    for el in a:
        if el != '' and el != "0":
            if conv is not None:
                el = conv(el)
            b.append(el)
    return b


def untis_split_first(s, conv=None):
    return clean_array(s.split(","), conv=conv)


def untis_split_second(s, conv=None):
    return clean_array(s.split("~"), conv=conv)


def untis_split_third(s, conv=None):
    return clean_array(s.split(";"), conv=conv)


DATE_FORMAT = "%Y%m%d"


def untis_date_to_date(untis):
    return timezone.datetime.strptime(str(untis), DATE_FORMAT)


def date_to_untis_date(date):
    return date.strftime(DATE_FORMAT)
