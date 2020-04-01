from haystack import indexes

# Not used here, but simplifies imports for apps
Indexable = indexes.Indexable  # noqa


class SearchIndex(indexes.SearchIndex):
    """ Base class for search indexes on AlekSIS models

    It provides a default document field caleld text and exects
    the related model in the model attribute.
    """

    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return self.model
