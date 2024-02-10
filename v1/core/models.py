from django.db import models
from v1.utils.abstract import CustomBaseAbstract, CoreBaseAbstract
from v1.commons.enums import AuthorType
from django.utils.translation import gettext_lazy as _
from v1.utils.managers import (
    JournalManager, InternetInfoManager, BookManager, ArticleManager, NewspaperManager, OfficialTextManager,
    OtherManager
)


class CapacityLevelOfTheAuditorium(CustomBaseAbstract):
    name = models.CharField(_("Salohiyat darajasi"), max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class TextType(CustomBaseAbstract):
    name = models.CharField(_("Matn tipi"), max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name}"


class FieldOfApplication(CustomBaseAbstract):
    name = models.CharField(_("Qo'llanish sohasi"), max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name}"


class LiteraryGenre(CustomBaseAbstract):
    name = models.CharField(_("Adabiy turi"), max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Style(CustomBaseAbstract):
    name = models.CharField(_("Uslub"), max_length=255)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Text(CoreBaseAbstract):
    # Newspaper
    number = models.CharField(_("Nashr raqami"), max_length=100, blank=True, null=True)
    net_address = models.CharField(_("NET-manzili"), max_length=500, blank=True, null=True)
    theme = models.CharField(_("Matn mavzusi"), max_length=255, blank=True, null=True)
    author = models.CharField(_("Muallif"), max_length=255, blank=True, null=True)
    author_type = models.CharField(
        _("Muallif jinsi"), choices=AuthorType.choices(), max_length=5, blank=True, null=True
    )
    wrote_at = models.DateTimeField(_("Yozilgan vaqti"), blank=True, null=True)
    published_at = models.DateTimeField(_("Nashr yili"), blank=True, null=True)
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, verbose_name=_("Uslubi"), blank=True, null=True)
    auditorium_age = models.CharField(_("Auditoriya yoshi"), max_length=10, blank=True, null=True)
    level_of_auditorium = models.ManyToManyField(
        CapacityLevelOfTheAuditorium, blank=True, verbose_name=_("Auditoriya salohiyat darajasi")
    )

    # official text
    document_type = models.CharField(_("Hujjat turi"), max_length=255, blank=True, null=True)
    document_owner = models.CharField(
        _("Hujjat chiqargan tashkilot (shaxs)"), max_length=255, blank=True, null=True
    )
    document_namely = models.CharField(_("Hujjat nomlanishi"), max_length=255, blank=True, null=True)

    # jurnal
    publisher = models.CharField(_("Nashriyoti"), max_length=300, blank=True, null=True)
    text_number = models.CharField(_("Adadi"), max_length=255, blank=True, null=True)
    issn = models.CharField(_("ISSN"), max_length=255, blank=True, null=True)
    text_type = models.ForeignKey(TextType, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name=_("Matn tipi"))

    # internet info
    field_of_application = models.ForeignKey(
        FieldOfApplication, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Qo'llanish sohasi")
    )

    # book
    authors = models.TextField(_("Mualliflar ismi, jinsi, yillari"), blank=True, null=True)
    literary_genre = models.ForeignKey(LiteraryGenre, on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name=_("Adabiy turi"))
    time_and_place_of_the_event = models.CharField(
        _("Voqea vaqti va joyi"), max_length=500, blank=True, null=True
    )
    isbn = models.CharField(_("ISBN"), max_length=255, blank=True, null=True)

    # article
    article_created_at = models.DateTimeField(_("Chop etilgan vaqti"), blank=True, null=True)
    pages_qty = models.PositiveIntegerField(_("Sahifalari"), blank=True, null=True)
    name_of_article = models.CharField(_("Manbaning (jurnal, kitob) nomi"), max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.source_type}"


class Newspaper(Text):

    objects = NewspaperManager()

    class Meta:
        proxy = True


class OfficialText(Text):
    objects = OfficialTextManager()

    class Meta:
        proxy = True


class Journal(Text):
    objects = JournalManager()

    class Meta:
        proxy = True


class InternetInfo(Text):
    objects = InternetInfoManager()

    class Meta:
        proxy = True


class Book(Text):
    objects = BookManager()

    class Meta:
        proxy = True


class Article(Text):
    objects = ArticleManager()

    class Meta:
        proxy = True


class Other(Text):
    objects = OtherManager()

    class Meta:
        proxy = True

# class Newspaper(CoreBaseAbstract):
#     number = models.CharField(_("Nashr raqami"), max_length=100, blank=True, null=True)
#     net_address = models.CharField(_("NET-manzili"), max_length=500)
#     theme = models.CharField(_("Matn mavzusi"), max_length=255)
#     author = models.CharField(_("Muallif"), max_length=255)
#     author_type = models.CharField(
#         _("Muallif jinsi"), choices=AuthorType.choices(), max_length=5, blank=True, null=True
#     )
#     wrote_at = models.DateTimeField(_("Yozilgan vaqti"), blank=True, null=True)
#     published_at = models.DateTimeField(_("Nashr yili"))
#     style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, verbose_name=_("Uslubi"))
#     auditorium_age = models.CharField(_("Auditoriya yoshi"), max_length=10, blank=True, null=True)
#     level_of_auditorium = models.ManyToManyField(
#         CapacityLevelOfTheAuditorium, blank=True, verbose_name=_("Auditoriya salohiyat darajasi")
#     )
#
#
# class OfficialText(CoreBaseAbstract):
#     net_address = models.CharField(_("NET-manzili"), max_length=500)
#     number = models.CharField(_("Hujjat raqami"), max_length=255, blank=True, null=True)
#     document_type = models.CharField(_("Hujjat turi"), max_length=255)
#     document_owner = models.CharField(
#         _("Hujjat chiqargan tashkilot (shaxs)"), max_length=255, blank=True, null=True
#     )
#     published_at = models.DateTimeField(_("E'lon qilingan vaqt"))
#     document_namely = models.CharField(_("Hujjat nomlanishi"), max_length=255, blank=True, null=True)
#
#
#
# class Journal(CoreBaseAbstract):
#     number = models.CharField(_("Nashr raqami"), max_length=255, blank=True, null=True)
#     net_address = models.CharField(_("NET-manzili"), max_length=500)
#     theme = models.CharField(_("Maqola mavzusi"), max_length=255)
#     author = models.CharField(_("Muallif"), max_length=255)
#     author_type = models.CharField(
#         _("Muallif jinsi"), choices=AuthorType.choices(), max_length=5, blank=True, null=True
#     )
#     wrote_at = models.DateTimeField(_("Yozilgan vaqti"), blank=True, null=True)
#     published_at = models.DateTimeField(_("Nashr yili"))
#     publisher = models.CharField(_("Nashriyoti"), max_length=300, blank=True, null=True)
#     text_number = models.CharField(_("Adadi"), max_length=255, blank=True, null=True)
#     issn = models.CharField(_("ISSN"), max_length=255, blank=True, null=True)
#     text_type = models.ForeignKey(TextType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Matn tipi"))
#     style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, verbose_name=_("Uslubi"))
#     auditorium_age = models.CharField(_("Auditoriya yoshi"), max_length=10, blank=True, null=True)
#     level_of_auditorium = models.ManyToManyField(
#         CapacityLevelOfTheAuditorium, blank=True, verbose_name=_("Auditoriya salohiyat darajasi")
#     )
#
#
# class InternetInfo(CoreBaseAbstract):
#     net_address = models.CharField(_("NET-manzili"), max_length=500)
#     author = models.CharField(_("Muallif"), max_length=255)
#     author_type = models.CharField(
#         _("Muallif jinsi"), choices=AuthorType.choices(), max_length=5, blank=True, null=True
#     )
#     wrote_at = models.DateTimeField(_("Yozilgan vaqti"), blank=True, null=True)
#     published_at = models.DateTimeField(_("Internetga joylangan vaqti"))
#     field_of_application = models.ForeignKey(
#         FieldOfApplication, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Qo'llanish sohasi")
#     )
#     text_type = models.ForeignKey(TextType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Matn tipi"))
#     style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, verbose_name=_("Uslubi"))
#     auditorium_age = models.CharField(_("Auditoriya yoshi"), max_length=10, blank=True, null=True)
#     level_of_auditorium = models.ManyToManyField(
#         CapacityLevelOfTheAuditorium, blank=True, verbose_name=_("Auditoriya salohiyat darajasi")
#     )
#
#
# class Book(CoreBaseAbstract):
#     authors = models.TextField(_("Mualliflar ismi, jinsi, yillari"))
#     wrote_at = models.DateTimeField(_("Yozilgan vaqti"), blank=True, null=True)
#     published_at = models.DateTimeField(_("Nashr yili"))
#     publisher = models.CharField(_("Nashriyoti"), max_length=300, blank=True, null=True)
#     text_number = models.CharField(_("Adadi"), max_length=255, blank=True, null=True)
#     isbn = models.CharField(_("ISBN"), max_length=255, blank=True, null=True)
#     text_type = models.ForeignKey(TextType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Matn tipi"))
#     literary_genre = models.ForeignKey(LiteraryGenre, on_delete=models.SET_NULL, null=True, verbose_name=_("Adabi turi"))
#     time_and_place_of_the_event = models.CharField(
#         _("Voqea vaqti va joyi"), max_length=500, blank=True, null=True
#     )
#     style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, verbose_name=_("Uslubi"))
#     auditorium_age = models.CharField(_("Auditoriya yoshi"), max_length=10, blank=True, null=True)
#     level_of_auditorium = models.ManyToManyField(
#         CapacityLevelOfTheAuditorium, blank=True, verbose_name=_("Auditoriya salohiyat darajasi")
#     )
#     field_of_application = models.ForeignKey(
#         FieldOfApplication, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Qo'llanish sohasi")
#     )
#
#
# class Article(CoreBaseAbstract):
#     authors = models.TextField(_("Mualliflar ismi, jinsi, yillari"))
#     article_created_at = models.DateTimeField(_("Chop etilgan vaqti"))
#     pages_qty = models.PositiveIntegerField(_("Sahifalari"))
#     name_of_article = models.CharField(_("Manbaning (jurnal, kitob) nomi"), max_length=255)
#     published_at = models.DateTimeField(_("Nashr yili"))
#     issn = models.CharField(_("ISSN"), max_length=255, blank=True, null=True)
#     net_address = models.CharField(_("NET-manzili"), max_length=500)
#     text_type = models.ForeignKey(TextType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Matn tipi"))
#     style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, verbose_name=_("Uslubi"))
#     auditorium_age = models.CharField(_("Auditoriya yoshi"), max_length=10, blank=True, null=True)
#     field_of_application = models.ForeignKey(
#         FieldOfApplication, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Qo'llanish sohasi")
#     )
#     level_of_auditorium = models.ManyToManyField(
#         CapacityLevelOfTheAuditorium, blank=True, verbose_name=_("Auditoriya salohiyat darajasi")
#     )
#
#
# class OtherMetaData(Book): ...
