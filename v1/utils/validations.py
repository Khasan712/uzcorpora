from django.core.exceptions import ValidationError


def validate_file_format_excel(value):
    if not value.name.endswith('.xlsx'):
        raise ValidationError('Only xlsx "excel" files are allowed.')


def validate_word_apostrophe(word: str):
    if "“" in word:
        word = word.replace("“", '"')
    if "”" in word:
        word = word.replace("”", '"')
    if "‘" in word:
        word = word.replace("‘", "'")
    if "’" in word:
        word = word.replace("’", "'")
    return word


def validate_text_apostrophe(word: str):
    return word.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")

