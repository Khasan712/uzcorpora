from v1.core.models import Text
import docx
import re
from celery import shared_task


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
        text = '\n'.join([para.text for para in paragraphs if para.text])
        obj.text = text
        obj.save()
    if obj.file_en:
        paragraphs = docx.Document(obj.file_en).paragraphs
        text = '\n'.join([para.text for para in paragraphs if para.text])
        obj.text_en = text
        obj.save()
    count_words_and_sentences.delay(obj_id)
