from rest_framework.validators import ValidationError


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
