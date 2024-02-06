from rest_framework import serializers
from v1.core.models import (
    CapacityLevelOfTheAuditorium, Newspaper
)
from rest_framework.validators import ValidationError
from v1.utils.tasks.core import pop_text_from_file


class CapacityLevelOfTheAuditoriumGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = CapacityLevelOfTheAuditorium
        fields = ('id', 'name')


class NewspaperMetaDataPostSerializer(serializers.ModelSerializer):
    level_of_auditorium = serializers.CharField(required=False)
    file = serializers.FileField(allow_empty_file=False, required=False)

    class Meta:
        model = Newspaper
        fields = (
            'id', 'name', 'corpus', 'text', 'file', 'number', 'net_address', 'theme', 'author',
            'author_type', 'wrote_at', 'published_at', 'style', 'auditorium_age', 'level_of_auditorium'
        )

        extra_kwargs = {
            'text': {'required': False}
        }

    def validate(self, attrs):
        data = super().validate(attrs)
        if (not data.get('file') and not data.get('text')) or (data.get('file') and data.get('text')):
            raise ValidationError({
                "status": False,
                "error": "File or text error"
            })

        file = data.get('file')
        if file and not str(file.name).endswith('.docx'):
            raise ValidationError({
                "status": False,
                "error": "File format error, upload only docx (word) format file!"
            })

        return data

    def create(self, validated_data):
        level_of_auditorium = validated_data.pop('level_of_auditorium')
        obj = super().create(validated_data)
        if level_of_auditorium and level_of_auditorium.replace(',', '').isdigit():
            obj.level_of_auditorium.set(CapacityLevelOfTheAuditorium.objects.filter(id__in=level_of_auditorium.split(',')))
            obj.save()

        if validated_data.get('file'):
            pop_text_from_file.delay('newspaper', obj.id)

        return obj

    def to_representation(self, instance):
        return {"status": True}
