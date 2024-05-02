from rest_framework.validators import ValidationError

from v1.commons.enums import CorpusChoice
from v1.core.models import CapacityLevelOfTheAuditorium


def raise_file_format_error(*files):
    for file in files:
        if file and not str(file.name).endswith('.docx'):
            raise ValidationError({
                "status": False,
                "error": "File format error, upload only docx (word) format file!"
            })


def raise_file_and_text_error(file=None, text=None):
    print(file)
    print(text)
    if (not file and not text) or (file and text):
        raise ValidationError({
            "status": False,
            "error": "File or text error"
        })


def raise_file_and_text_error_en(corpus, file=None, text=None, file_en=None, text_en=None, file_tr=None, text_tr=None):
    raise_file_and_text_error(file, text)
    if corpus.key != list(CorpusChoice.choices())[0][1]:
        if file_en or text_en or file_tr or text_tr:
            raise ValidationError({
                "status": False,
                "error": "You can not upload other language files or text, please select parallel corpus!"
            })
    if file_en and text_en:
        raise ValidationError({
            "status": False,
            "error": "You can not upload 'file en' and 'text en' in the same time!"
        })
    if file_tr and text_tr:
        raise ValidationError({
            "status": False,
            "error": "You can not upload 'file tr' and 'text tr' in the same time!"
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
