from django.contrib import admin
from v1.core.models import (
    CapacityLevelOfTheAuditorium, TextType, FieldOfApplication, LiteraryGenre, Newspaper, OfficialText,
    Journal, InternetInfo, Book, Article, Other, Style, Phrase, Word, WordGrammar, WordSemanticExpression,
    CreateWordFromExcel, ParagraphOfText, Text, Language, LangText
)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'is_main', 'created_at', 'updated_at')


@admin.register(LangText)
class LangTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'lang', 'word_qty', 'sentence_qty', 'created_at', 'updated_at')


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'corpus', 'word_qty', 'sentence_qty', 'created_at', 'updated_at', 'creator')


@admin.register(ParagraphOfText)
class ParagraphOfTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'order_num', 'created_at', 'is_active')


@admin.register(CreateWordFromExcel)
class CreateWordFromExcelAdmin(admin.ModelAdmin):
    list_display = ('id', 'phrase', 'word_phrase', 'file', 'get_total_words')
    autocomplete_fields = ['phrase']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('phrase')


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'phrase', 'word')


@admin.register(WordGrammar)
class WordGrammarAdmin(admin.ModelAdmin):
    list_display = ('id', 'phrase', 'word')


@admin.register(WordSemanticExpression)
class WordSemanticExpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'phrase', 'word')


@admin.register(Phrase)
class PhrasesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    search_fields = ('id', 'name', 'parent__name')


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')


@admin.register(CapacityLevelOfTheAuditorium)
class CapacityLevelOfTheAuditoriumAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'parent', 'created_at', 'updated_at')


@admin.register(TextType)
class TextTypeAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'created_at', 'updated_at')


@admin.register(FieldOfApplication)
class FieldOfApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'created_at', 'updated_at')


@admin.register(LiteraryGenre)
class LiteraryGenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", 'created_at', 'updated_at')


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'corpus', 'word_qty', 'sentence_qty', 'created_at', 'updated_at')


@admin.register(OfficialText)
class OfficialTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'corpus', 'word_qty', 'sentence_qty', 'created_at', 'updated_at')


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'corpus', 'word_qty', 'sentence_qty', 'created_at', 'updated_at')


@admin.register(InternetInfo)
class InternetInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'corpus', 'word_qty', 'sentence_qty', 'created_at', 'updated_at')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'corpus', 'word_qty', 'sentence_qty', 'created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.role != 'admin':
            return queryset.filter(creator_id=request.user.id)
        return queryset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'corpus', 'word_qty', 'sentence_qty', 'created_at', 'updated_at')


@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'corpus', 'word_qty', 'sentence_qty', 'created_at', 'updated_at')


