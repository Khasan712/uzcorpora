from django.contrib import admin
from v1.corpus.models import Corpus


@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at', 'parent')


