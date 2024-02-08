from rest_framework import serializers
from v1.core.models import (
    CapacityLevelOfTheAuditorium, Text
)

from v1.utils.raise_errors import raise_file_format_error, raise_file_and_text_error


class CapacityLevelOfTheAuditoriumGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = CapacityLevelOfTheAuditorium
        fields = ('id', 'name')


class TextPostBaseSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        raise_file_and_text_error(data.get('file'), data.get('text'))

        raise_file_format_error(data.get('file'))

        return data

    def to_representation(self, instance):
        return {"status": True}


class NewspaperMetaDataPostSerializer(TextPostBaseSerializer):
    level_of_auditorium = serializers.CharField(required=False)
    file = serializers.FileField(allow_empty_file=False, required=False)

    class Meta:
        model = Text
        fields = (
            'id', 'name', 'corpus', 'text', 'file', 'source_type', 'number', 'net_address', 'theme', 'author',
            'author_type', 'wrote_at', 'published_at', 'style', 'auditorium_age', 'level_of_auditorium'
        )

        extra_kwargs = {
            'text': {'required': False}
        }

    def create(self, validated_data):
        level_of_auditorium = validated_data.pop('level_of_auditorium')
        obj = super().create(validated_data)
        if level_of_auditorium and level_of_auditorium.replace(',', '').isdigit():
            obj.level_of_auditorium.set(CapacityLevelOfTheAuditorium.objects.filter(id__in=level_of_auditorium.split(',')))
            obj.save()

        return obj
