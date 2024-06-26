from django.db import models
from v1.utils.abstract import CustomBaseAbstract, CoreBaseAbstract
from v1.commons.enums import AuthorType, WordPhrase, Lang
from django.utils.translation import gettext_lazy as _
from v1.utils.managers import (
    JournalManager, InternetInfoManager, BookManager, ArticleManager, NewspaperManager, OfficialTextManager,
    OtherManager
)
from v1.utils.validations import validate_file_format_excel


class Language(CustomBaseAbstract):
    """
    Tillar
    """
    name = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'K) Tillar'

    def __str__(self):
        return f'{self.id} - {self.name}'


class LangText(CustomBaseAbstract):
    """
    Har bitta til uchun kiritilgan matn
    """
    text_obj = models.ForeignKey('core.Text', on_delete=models.SET_NULL, null=True)
    lang = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='core/files/', blank=True, null=True)
    word_qty = models.PositiveIntegerField(default=0)
    sentence_qty = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'J) Matnlar'

    def __str__(self):
        return f"{self.id} - {self.lang.name}"


class Phrase(CustomBaseAbstract):
    """
    So'z turkumlari
    """
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        parent = self.parent.id if self.parent else None
        return f'{self.id} - {self.name} - Parent => : {parent}'


class Word(CustomBaseAbstract):
    """
    So'z bazasi modeli
    """
    phrase = models.ForeignKey(Phrase, on_delete=models.SET_NULL, null=True)
    word = models.CharField(max_length=255)
    lemma = models.CharField(max_length=255)
    uuid = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.word} - {self.phrase.id}"


class WordGrammar(CustomBaseAbstract):
    """
    So'z grammatikasi - bittaga ko'p
    """
    word = models.ForeignKey(Word, on_delete=models.SET_NULL, null=True, related_name='word_grammars')
    phrase = models.ForeignKey(Phrase, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('word', 'phrase')

    def __str__(self):
        try:
            return f"{self.id} - {self.word.word} - {self.phrase.id}"
        except:
            return super().__str__()
        

class WordSemanticExpression(CustomBaseAbstract):
    """
    So'zning simmantik ifodasi - bittaga ko'p
    """
    word = models.ForeignKey(Word, on_delete=models.SET_NULL, null=True, related_name='word_semantic_expressions')
    phrase = models.ForeignKey(Phrase, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('word', 'phrase')

    def __str__(self):
        try:
            return f"{self.id} - {self.word.word} - {self.phrase.id}"
        except:
            return super().__str__()


class CreateWordFromExcel(CustomBaseAbstract):
    """
    So'zlarni excel fayldan o'qib yaratish modeli
    """
    phrase = models.ForeignKey(Phrase, on_delete=models.SET_NULL, null=True)
    word_phrase = models.CharField(max_length=50, choices=WordPhrase.choices())
    file = models.FileField(upload_to='create_word_from_file/', validators=[validate_file_format_excel])
    uuid = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.word_phrase}"

    def get_total_words(self):
        if self.uuid:
            return Word.objects.filter(uuid=self.uuid).count()
        return 0


class CapacityLevelOfTheAuditorium(CustomBaseAbstract):
    """
    Salohiyat darajasi
    """
    name = models.CharField(_("Salohiyat darajasi"), max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'I) Auditoriya yosh salohiyati'

    def __str__(self):
        return f'{self.id} - {self.name}'


class TextType(CustomBaseAbstract):
    """
    Matn tipi
    """
    name = models.CharField(_("Matn tipi"), max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name}"


class FieldOfApplication(CustomBaseAbstract):
    """
    Qo'llanish sahasi
    """
    name = models.CharField(_("Qo'llanish sohasi"), max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name}"


class LiteraryGenre(CustomBaseAbstract):
    """
    Adabiy tur
    """
    name = models.CharField(_("Adabiy turi"), max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Style(CustomBaseAbstract):
    """
    Uslubi
    """
    name = models.CharField(_("Uslub"), max_length=255)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Text(CoreBaseAbstract):
    """
    Meta ma'lumot
    """
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
    pages_qty = models.CharField(_("Sahifalari"), blank=True, null=True)
    name_of_article = models.CharField(_("Manbaning (jurnal, kitob) nomi"), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "A) Matnlar | Meta ma'lumot"

    def __str__(self):
        return f"{self.id} - {self.source_type}"


class ParagraphOfText(CustomBaseAbstract):
    """
    Matn ichidagi abzatslar alohida obyekt bo'lib saqlanadi va har bitta abzats shu modelning instance bo'ladi
    """
    text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True)
    lang_text = models.ForeignKey(LangText, on_delete=models.SET_NULL, blank=True, null=True)
    paragraph = models.TextField()
    uuid = models.CharField(max_length=250, blank=True, null=True)
    order_num = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id} - {len(str(self.paragraph))}'


class Newspaper(Text):

    objects = NewspaperManager()

    class Meta:
        proxy = True
        verbose_name_plural = 'B) Gazetalar'


class OfficialText(Text):
    objects = OfficialTextManager()

    class Meta:
        proxy = True
        verbose_name_plural = 'C) Rasmiy matnlar'


class Journal(Text):
    objects = JournalManager()

    class Meta:
        proxy = True
        verbose_name_plural = 'D) Jurnallar'


class InternetInfo(Text):
    objects = InternetInfoManager()

    class Meta:
        proxy = True
        verbose_name_plural = 'E) E-ma\'lumotlar'


class Book(Text):
    objects = BookManager()

    class Meta:
        proxy = True
        verbose_name_plural = 'F) Kitoblar'


class Article(Text):
    objects = ArticleManager()

    class Meta:
        proxy = True
        verbose_name_plural = 'G) Maqolalar'


class Other(Text):
    objects = OtherManager()

    class Meta:
        proxy = True
        verbose_name_plural = 'H) Boshqalar'

