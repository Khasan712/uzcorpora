from rest_framework.validators import ValidationError

from v1.core.models import CapacityLevelOfTheAuditorium


def raise_file_format_error(file=None):
    if file and not str(file.name).endswith('.docx'):
        raise ValidationError({
            "status": False,
            "error": "File format error, upload only docx (word) format file!"
        })


def raise_file_and_text_error(file=None, text=None):
    if (not file and not text) or (file and text):
        raise ValidationError({
            "status": False,
            "error": "File or text error"
        })


def get_or_raise_level_of_auditorium(level_of_auditorium=None):
    if level_of_auditorium and level_of_auditorium.replace(',', '').isdigit():
        data = CapacityLevelOfTheAuditorium.objects.filter(id__in=level_of_auditorium.split(','))
        if data.count() != len(level_of_auditorium.split(',')):
            raise ValidationError({
                "status": False,
                "error": "There are, does not exist pk in level of auditorium"
            })
        return data
