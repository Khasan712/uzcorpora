from django.db.models.query import QuerySet
from django.db.models.manager import BaseManager


class NewspaperManager(BaseManager.from_queryset(QuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(source_type='newspaper')


class OfficialTextManager(BaseManager.from_queryset(QuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(source_type='official_text')


class JournalManager(BaseManager.from_queryset(QuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(source_type='journal')


class InternetInfoManager(BaseManager.from_queryset(QuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(source_type='internet_info')


class BookManager(BaseManager.from_queryset(QuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(source_type='book')


class ArticleManager(BaseManager.from_queryset(QuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(source_type='article')


class OtherManager(BaseManager.from_queryset(QuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(source_type='other')

