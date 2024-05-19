from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError
from v1.commons.enums import CorpusChoice
from v1.core.models import (
    CapacityLevelOfTheAuditorium, Text, Style, TextType, FieldOfApplication, LiteraryGenre, Language, LangText
)
from v1.utils.constants import FILE_TYPE, TEXT_TYPE
from v1.utils.fields import GENERAL_TEXT_FIELDS
from v1.utils.file_services import get_file_paragraphs_qty
from v1.utils.raise_errors import (get_or_raise_level_of_auditorium, raise_file_and_text_error)
from v1.utils.tasks.core import text_validate_and_config_task
from v1.corpus.serializers import CorpusGetSerializer


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name', 'description', 'is_main', 'created_at', 'updated_at')


class LiteraryGenreGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiteraryGenre
        fields = ('id', 'name', 'parent')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        if res.get('parent'):
            res['parent'] = {
                'id': instance.parent.id,
                'name': instance.parent.name,
            }
        return res


class FieldOfApplicationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfApplication
        fields = ('id', 'name')


class TextTypeGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextType
        fields = ('id', 'name')


class TextGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ("id", "name", 'corpus', 'source_type', 'created_at', 'updated_at')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['corpus'] = {
            "id": instance.corpus.id,
            "name": instance.corpus.name
        }
        res['word_qty'] = getattr(instance, 'word_qty', 0)
        res['sentence_qty'] = getattr(instance, 'sentence_qty', 0)
        res['text_file'] = FILE_TYPE if getattr(instance, 'file', None) else TEXT_TYPE
        res['creator'] = {
            'id': instance.creator.id,
            'first_name': instance.creator.first_name,
            'phone_number': instance.creator.phone_number,
        } if instance.creator else None
        try:
            res['source_type_description'] = instance.source_type_description
        except:
            pass
        return res


class StyleGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ('id', 'name')


class CapacityLevelOfTheAuditoriumGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = CapacityLevelOfTheAuditorium
        fields = ('id', 'name')


class TextPostBaseSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        level_of_auditorium = get_or_raise_level_of_auditorium(data.get('level_of_auditorium'))
        if level_of_auditorium:
            data.pop('level_of_auditorium')
            self.context['level_of_auditorium'] = level_of_auditorium
        return data

    def to_representation(self, instance):
        if self.context['request'].method == 'GET' and self.context.get('kwargs').get('pk'):
            res = super().to_representation(instance)
            res['corpus'] = CorpusGetSerializer(instance.corpus).data
            if res['corpus']['key'] == list(CorpusChoice.choices())[0][1]:
                res['file_en'] = instance.file_en
            if res.get('style'):
                res['style'] = StyleGetSerializer(instance.style).data
            if res.get('text_type'):
                res['text_type'] = TextTypeGetSerializer(instance.text_type).data
            if res.get('field_of_application'):
                res['field_of_application'] = FieldOfApplicationGetSerializer(instance.field_of_application).data
            if res.get('literary_genre'):
                res['literary_genre'] = LiteraryGenreGetSerializer(instance.literary_genre).data
            if res.get('level_of_auditorium'):
                res['level_of_auditorium'] = CapacityLevelOfTheAuditoriumGetSerializer(
                    instance.level_of_auditorium.all(), many=True
                ).data
            return res
        return {"status": True}

    def get_text_or_file_and_save(self, text_obj, parallel_corpus=None):
        fields = self.context['request'].data
        langs = Language.objects.filter(is_active=True)
        if not parallel_corpus:
            langs = langs.filter(is_main=True)
        text_or_file = []
        line_qty = 0
        for lang in langs:
            text = fields.get(f'text_{lang.name}', None)
            file = fields.get(f'file_{lang.name}', None)
            raise_file_and_text_error(file, text)
            if text:
                if line_qty == 0:
                    line_qty = len(text.split('\n\n'))
                elif line_qty != len(text.split('\n\n')):
                    raise ValidationError({'error': 'The texts number of lines have to be the same!'})
                text_or_file.append(
                    LangText(text_obj=text_obj, lang_id=lang.id, text=text, file=file)
                )
            elif file:
                file_paragraphs_qty = get_file_paragraphs_qty(file)
                if line_qty == 0:
                    line_qty = file_paragraphs_qty
                elif line_qty != file_paragraphs_qty:
                    raise ValidationError({'error': 'The files number of lines have to be the same!'})
                text_or_file.append(
                    LangText(text_obj=text_obj, lang_id=lang.id, text=text, file=file)
                )
        if not text_or_file:
            raise ValidationError({'error': 'No file or text found!'})
        LangText.objects.bulk_create(text_or_file)

    def create(self, validated_data):
        with transaction.atomic():
            obj = super().create(validated_data)
            parallel_corpus = True if obj.corpus.key == list(CorpusChoice.choices())[0][1] else None
            self.get_text_or_file_and_save(obj, parallel_corpus)
            level_of_auditorium = self.context.get('level_of_auditorium')
            if level_of_auditorium:
                obj.level_of_auditorium.set(level_of_auditorium)
                obj.save()
        text_validate_and_config_task.delay(obj.id)
        return obj


class NewspaperMetaDataPostSerializer(TextPostBaseSerializer):
    level_of_auditorium = serializers.CharField(required=False)

    class Meta:
        model = Text
        fields = [
            'number', 'net_address', 'theme', 'author', 'author_type', 'wrote_at',
            'published_at', 'style', 'auditorium_age', 'level_of_auditorium',
        ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'name': {'required': True},
            'theme': {'required': True},
            'author': {'required': True},
            'style': {'required': True},
            'net_address': {'required': True},
            'corpus': {'required': True},
        }


class OfficialTextMetaDataPostSerializer(TextPostBaseSerializer):

    class Meta:
        model = Text
        fields = [
            'number', 'net_address', 'document_type', 'document_owner', 'published_at',
        ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'document_type': {'required': True},
            'name': {'required': True},
            'published_at': {'required': True},
            'net_address': {'required': True},
            'corpus': {'required': True},
        }


class JournalMetaDataPostSerializer(TextPostBaseSerializer):
    level_of_auditorium = serializers.CharField(required=False)

    class Meta:
        model = Text
        fields = [
            'number', 'net_address', 'theme', 'author', 'author_type', 'wrote_at', 'published_at', 'publisher',
            'text_number', 'issn', 'text_type', 'style', 'auditorium_age', 'level_of_auditorium',
         ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'name': {'required': True},
            'theme': {'required': True},
            'author': {'required': True},
            'published_at': {'required': True},
            'style': {'required': True},
            'net_address': {'required': True},
            'corpus': {'required': True},
        }


class InternetInfoMetaDataPostSerializer(TextPostBaseSerializer):
    level_of_auditorium = serializers.CharField(required=False)

    class Meta:
        model = Text
        fields = [
            'net_address', 'author', 'author_type', 'wrote_at', 'published_at', 'field_of_application',
            'text_type', 'style', 'auditorium_age', 'level_of_auditorium', 'literary_genre'
        ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'name': {'required': True},
            'author': {'required': True},
            'published_at': {'required': True},
            'style': {'required': True},
            'net_address': {'required': True},
            'corpus': {'required': True},
        }


class BookMetaDataPostSerializer(TextPostBaseSerializer):
    level_of_auditorium = serializers.CharField(required=False)

    class Meta:
        model = Text
        fields = [
            'authors', 'wrote_at', 'published_at', 'publisher', 'text_number', 'isbn', 'text_type',
            'literary_genre', 'time_and_place_of_the_event', 'style', 'auditorium_age', 'level_of_auditorium',
            'field_of_application', 'net_address'
        ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'name': {'required': True},
            'authors': {'required': True},
            'literary_genre': {'required': True},
            'style': {'required': True},
            'corpus': {'required': True},
        }


class ArticleMetaDataPostSerializer(TextPostBaseSerializer):
    level_of_auditorium = serializers.CharField(required=False)

    class Meta:
        model = Text
        fields = [
            'authors', 'article_created_at', 'pages_qty', 'name_of_article', 'published_at', 'issn', 'net_address',
            'text_type', 'style', 'auditorium_age', 'level_of_auditorium', 'field_of_application',
        ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'name': {'required': True},
            'authors': {'required': True},
            'article_created_at': {'required': True},
            'name_of_article': {'required': True},
            'style': {'required': True},
            'corpus': {'required': True},
        }

