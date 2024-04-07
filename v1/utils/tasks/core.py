from v1.core.models import Text, ParagraphOfText
import docx
import re
from celery import shared_task

from v1.utils.validations import validate_text_apostrophe


def save_paragraph_of_text(paragraphs, text_obj_id):
    text = ''
    paragraphs_obj = []
    for paragraph in paragraphs:
        if paragraph.text:
            validated_text = validate_text_apostrophe(paragraph.text).strip()
            text += f'{validated_text}\n'
            paragraphs_obj.append(ParagraphOfText(text_id=text_obj_id, paragraph=validated_text))
    ParagraphOfText.objects.bulk_create(paragraphs_obj)
    return text


@shared_task()
def count_words_and_sentences(obj_id):
    obj = Text.objects.get(id=obj_id)
    sentence_enders_pattern = r'[.!?]|\.'
    if obj.text:
        sentences = re.split(sentence_enders_pattern, obj.text)
        obj.sentence_qty = len(sentences)
        obj.word_qty = len(obj.text.split())
        obj.save()
    if obj.text_en:
        sentences = re.split(sentence_enders_pattern, obj.text_en)
        obj.sentence_qty_en = len(sentences)
        obj.word_qty_en = len(obj.text_en.split())
        obj.save()


@shared_task()
def pop_text_from_file(obj_id):
    obj = Text.objects.get(id=obj_id)
    if obj.file:
        paragraphs = docx.Document(obj.file).paragraphs
        obj.text = save_paragraph_of_text(paragraphs, obj.id)
        obj.save()
    if obj.file_en:
        paragraphs = docx.Document(obj.file_en).paragraphs
        obj.text = save_paragraph_of_text(paragraphs, obj.id)
        obj.save()
    count_words_and_sentences.delay(obj_id)
