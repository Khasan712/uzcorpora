from v1.core.models import Text, ParagraphOfText
import docx
import re
from celery import shared_task

from v1.utils.validations import validate_text_apostrophe


def save_paragraph_of_text(paragraphs, text_obj_id, lang='uz'):
    text = ''
    paragraphs_obj = []
    for paragraph in paragraphs:
        if paragraph.text:
            validated_text = validate_text_apostrophe(paragraph.text).strip()
            text += f'{validated_text}\n'
            paragraphs_obj.append(ParagraphOfText(text_id=text_obj_id, paragraph=validated_text, lang=lang))
    ParagraphOfText.objects.bulk_create(paragraphs_obj)
    return text


def save_text_of_paragraphs(paragraphs: str, text_obj_id, lang='uz'):
    text = ''
    paragraphs_obj = []
    for paragraph in paragraphs.splitlines():
        paragraph = paragraph.strip()
        if paragraph:
            validated_text = validate_text_apostrophe(paragraph)
            paragraphs_obj.append(ParagraphOfText(text_id=text_obj_id, paragraph=validated_text, lang=lang))
            text += f'{validated_text}\n'
    ParagraphOfText.objects.bulk_create(paragraphs_obj)
    return text


@shared_task()
def count_words_and_sentences(obj_id):
    obj = Text.objects.get(id=obj_id)
    sentence_enders_pattern = r'[.!?]|\.'
    if obj.text:
        if not obj.file:
            obj.text = save_text_of_paragraphs(obj.text, obj_id)
            obj.save()
        sentences = re.split(sentence_enders_pattern, obj.text)
        obj.sentence_qty = len(sentences)
        obj.word_qty = len(obj.text.split())
        obj.save()
    if obj.text_en:
        if not obj.file_en:
            obj.text = save_text_of_paragraphs(obj.text, obj_id, 'en')
            obj.save()
        sentences = re.split(sentence_enders_pattern, obj.text_en)
        obj.sentence_qty_en = len(sentences)
        obj.word_qty_en = len(obj.text_en.split())
        obj.save()


@shared_task()
def pop_text_from_file(obj_id):
    obj = Text.objects.get(id=obj_id)
    if obj.file:
        paragraphs = docx.Document(obj.file).paragraphs
        obj.text = save_paragraph_of_text(paragraphs, obj_id)
        obj.save()
    if obj.file_en:
        paragraphs = docx.Document(obj.file_en).paragraphs
        obj.text = save_paragraph_of_text(paragraphs, obj_id, 'en')
        obj.save()
    count_words_and_sentences.delay(obj_id)
