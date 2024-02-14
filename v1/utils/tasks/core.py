from v1.core.models import Text
import docx
import re
from celery import shared_task


@shared_task()
def count_words_and_sentences(obj_id):
    obj = Text.objects.get(id=obj_id)
    sentence_enders_pattern = r'[.!?]|\.'
    sentences = re.split(sentence_enders_pattern, obj.text)
    # three_dots = len(obj.text.split('...'))
    # with_q = len(obj.text.split('?'))
    # with_1 = len(obj.text.split('!'))
    # with_dot = len(obj.text.split('.'))
    #
    # total_sentence_qty = abs(three_dots - with_dot) + with_q + with_1
    # obj.sentence_qty = total_sentence_qty
    obj.sentence_qty = len(sentences)
    obj.word_qty = len(obj.text.split())
    obj.save()


@shared_task()
def pop_text_from_file(obj_id):
    obj = Text.objects.get(id=obj_id)
    paragraphs = docx.Document(obj.file).paragraphs
    text = '\n'.join([para.text for para in paragraphs if para.text])
    obj.text = text
    obj.save()
    count_words_and_sentences.delay(obj_id)
