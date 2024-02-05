from django.contrib import admin
from v1.core.models import (
    CapacityLevelOfTheAuditorium, TextType, FieldOfApplication, LiteraryGenre, Newspaper, OfficialText,
    Journal, InternetInfo, Book, Article, OtherMetaData
)


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


@admin.register(OtherMetaData)
class OtherMetaDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'corpus', 'word_qty', 'sentence_qty', 'created_at', 'updated_at')


