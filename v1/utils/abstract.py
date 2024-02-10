from django.db import models
from django.utils.translation import gettext_lazy as _

from v1.commons.enums import SourceType


class CustomBaseAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CoreBaseAbstract(CustomBaseAbstract):
    creator = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    name = models.CharField(_("Nomi"), max_length=255)
    corpus = models.ForeignKey('corpus.Corpus', on_delete=models.SET_NULL, verbose_name=_("Korpus turi"), null=True)
    word_qty = models.PositiveIntegerField(_("So'z miqdori"), default=0)
    sentence_qty = models.PositiveIntegerField(_("Gap miqdori"), default=0)
    text = models.TextField(_("Matn"), blank=True, null=True)
    file = models.FileField(upload_to='core/', blank=True, null=True)
    source_type = models.CharField(_("Manba turi"), choices=SourceType.choices(), max_length=17)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id} - {self.name}"
