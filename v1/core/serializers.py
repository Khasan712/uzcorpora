from rest_framework import serializers
from v1.core.models import (
    CapacityLevelOfTheAuditorium, Text, Style, TextType, FieldOfApplication, LiteraryGenre
)

from v1.utils.raise_errors import (
    raise_file_format_error, raise_file_and_text_error, get_or_raise_level_of_auditorium
)


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
    file = serializers.FileField(allow_empty_file=False, required=False)

    def validate(self, attrs):
        data = super().validate(attrs)

        raise_file_and_text_error(data.get('file'), data.get('text'))

        raise_file_format_error(data.get('file'))

        level_of_auditorium = get_or_raise_level_of_auditorium(data.get('level_of_auditorium'))

        if level_of_auditorium:
            data.pop('level_of_auditorium')
            self.context['level_of_auditorium'] = level_of_auditorium

        return data

    def to_representation(self, instance):
        return {"status": True}

    def create(self, validated_data):
        obj = super().create(validated_data)
        level_of_auditorium = self.context.get('level_of_auditorium')
        if level_of_auditorium:
            obj.level_of_auditorium.set(level_of_auditorium)
            obj.save()
        return obj


class NewspaperMetaDataPostSerializer(TextPostBaseSerializer):
    level_of_auditorium = serializers.CharField(required=False)

    class Meta:
        model = Text
        fields = (
            'id', 'name', 'corpus', 'text', 'file', 'source_type',
            'number', 'net_address', 'theme', 'author', 'author_type', 'wrote_at',
            'published_at', 'style', 'auditorium_age', 'level_of_auditorium'
        )

        extra_kwargs = {
            'text': {'required': False},
            'name': {'required': True},
            'theme': {'required': True},
            'author': {'required': True},
            'wrote_at': {'required': True},
            'style': {'required': True},
            'net_address': {'required': True},
            'corpus': {'required': True},
        }


class OfficialTextMetaDataPostSerializer(TextPostBaseSerializer):

    class Meta:
        model = Text
        fields = (
            'id', 'name', 'corpus', 'text', 'file', 'source_type',
            'number', 'net_address', 'document_type', 'document_owner', 'published_at'
        )

        extra_kwargs = {
            'text': {'required': False},
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
        fields = (
            'id', 'name', 'corpus', 'text', 'file', 'source_type',
            'number', 'net_address', 'theme', 'author', 'author_type', 'wrote_at', 'published_at', 'publisher',
            'text_number', 'issn', 'text_type', 'style', 'auditorium_age', 'level_of_auditorium'
        )

        extra_kwargs = {
            'text': {'required': False},
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
        fields = (
            'id', 'name', 'corpus', 'text', 'file', 'source_type',
            'net_address', 'author', 'author_type', 'wrote_at', 'published_at', 'field_of_application',
            'text_type', 'style', 'auditorium_age', 'level_of_auditorium'
        )

        extra_kwargs = {
            'text': {'required': False},
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
        fields = (
            'id', 'name', 'corpus', 'text', 'file', 'source_type',
            'authors', 'wrote_at', 'published_at', 'publisher', 'text_number', 'isbn', 'text_type',
            'literary_genre', 'time_and_place_of_the_event', 'style', 'auditorium_age', 'level_of_auditorium',
            'field_of_application'
        )

        extra_kwargs = {
            'text': {'required': False},
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
        fields = (
            'id', 'name', 'corpus', 'text', 'file', 'source_type',
            'authors', 'article_created_at', 'pages_qty', 'name_of_article', 'published_at', 'issn', 'net_address',
            'text_type', 'style', 'auditorium_age', 'level_of_auditorium', 'field_of_application'
        )

        extra_kwargs = {
            'text': {'required': False},
            'name': {'required': True},
            'authors': {'required': True},
            'article_created_at': {'required': True},
            'pages_qty': {'required': True},
            'name_of_article': {'required': True},
            'style': {'required': True},
            'corpus': {'required': True},
        }


