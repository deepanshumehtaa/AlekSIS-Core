from haystack import indexes

from .models import Person, Group


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    first_name = indexes.CharField(model_attr="first_name")
    last_name = indexes.CharField(model_attr="last_name")
    additional_name = indexes.CharField(model_attr="additional_name")
    email = indexes.CharField(model_attr="email")
    phone_number = indexes.CharField(model_attr="phone_number")
    mobile_number = indexes.CharField(model_attr="mobile_number")

    def get_model(self):
        return Person


class GroupIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    name = indexes.CharField(model_attr="name")
    short_name = indexes.CharField(model_attr="short_name")

    def get_model(self):
        return Group
