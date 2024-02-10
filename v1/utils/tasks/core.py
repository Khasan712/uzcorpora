from v1.core.models import Text
import docx
import re
from celery import shared_task


@shared_task()
def count_words_and_sentences(obj_id):
    obj = Text.objects.get(id=obj_id)
    sentence_enders_pattern = r'[.!?]|\.\.\.'
    sentences = re.split(sentence_enders_pattern, obj.text)
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
