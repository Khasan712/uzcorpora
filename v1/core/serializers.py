from rest_framework import serializers
from django.db import transaction
from v1.commons.enums import CorpusChoice
from v1.core.models import (
    CapacityLevelOfTheAuditorium, Text, Style, TextType, FieldOfApplication, LiteraryGenre, Language
)
from v1.utils.constants import FILE_TYPE, TEXT_TYPE
from v1.utils.fields import GENERAL_TEXT_FIELDS
from v1.utils.raise_errors import (
    raise_file_format_error, get_or_raise_level_of_auditorium, raise_file_and_text_error_en
)
from v1.corpus.serializers import CorpusGetSerializer


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
        fields = ("id", "name", 'corpus', 'source_type', 'word_qty', 'sentence_qty', 'created_at', 'updated_at')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['corpus'] = {
            "id": instance.corpus.id,
            "name": instance.corpus.name
        }
        res['text_file'] = FILE_TYPE if instance.file else TEXT_TYPE
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

        if self.context['request'].method == 'POST':
            raise_file_and_text_error_en(
                data.get('corpus'),  data.get('file'), data.get('text'),
                data.get('file_en'), data.get('text_en'), data.get('file_tr'), data.get('text_tr'),
            )
            raise_file_format_error(data.get('file'), data.get('file_en'), data.get('file_tr'))

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

    def get_text_or_file_and_save(self, text_obj):
        fields = self.context['request'].data
        langs = Language.objects.filter(is_active=True)
        text_or_file = []
        for lang in langs:
            pass

    def create(self, validated_data):
        with transaction.atomic():
            obj = super().create(validated_data)
            level_of_auditorium = self.context.get('level_of_auditorium')
            if level_of_auditorium:
                obj.level_of_auditorium.set(level_of_auditorium)
                obj.save()
            # raise ValueError
        return obj


class NewspaperMetaDataPostSerializer(TextPostBaseSerializer):
    level_of_auditorium = serializers.CharField(required=False)

    class Meta:
        model = Text
        fields = [
            'number', 'net_address', 'theme', 'author', 'author_type', 'wrote_at',
            'published_at', 'style', 'auditorium_age', 'level_of_auditorium'
        ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'text': {'write_only': True},
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
            'number', 'net_address', 'document_type', 'document_owner', 'published_at'
        ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'text': {'write_only': True},
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
            'text_number', 'issn', 'text_type', 'style', 'auditorium_age', 'level_of_auditorium'
         ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'text': {'write_only': True},
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
            'text_type', 'style', 'auditorium_age', 'level_of_auditorium'
        ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'text': {'write_only': True},
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
            'field_of_application' 'net_address'
        ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'text': {'write_only': True},
            'name': {'required': True},
            'authors': {'required': True},
            'published_at': {'required': True},
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
            'text_type', 'style', 'auditorium_age', 'level_of_auditorium', 'field_of_application'
        ] + GENERAL_TEXT_FIELDS

        extra_kwargs = {
            'text': {'write_only': True},
            'name': {'required': True},
            'authors': {'required': True},
            'article_created_at': {'required': True},
            'pages_qty': {'required': True},
            'name_of_article': {'required': True},
            'style': {'required': True},
            'corpus': {'required': True},
        }


