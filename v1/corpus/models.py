from django.db import models
from v1.commons.enums import CorpusChoice
from v1.utils.abstract import CustomBaseAbstract


class Corpus(CustomBaseAbstract):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    key = models.CharField(max_length=100, choices=CorpusChoice.choices(), default='other')

    def __str__(self):
        return f'{self.id} - {self.name}'

