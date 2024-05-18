from v1.core.models import ParagraphOfText, LangText
import docx
import re
from celery import shared_task
from v1.utils.validations import validate_text_apostrophe


def get_text_from_paragraphs(file):
    paragraphs = docx.Document(file).paragraphs
    text = ''
    for paragraph in paragraphs:
        text += f'{paragraph.text}\n'
    return text.strip()


def save_text_of_paragraphs(paragraphs: str, lang_text_id, text_obj_id):
    text = ''
    paragraphs_obj = []
    order_num = 1
    for paragraph in paragraphs.split('\n\n'):
        paragraph = paragraph.strip()
        if paragraph:
            validated_text = validate_text_apostrophe(paragraph).strip()
            paragraphs_obj.append(ParagraphOfText(
                text_id=text_obj_id, lang_text_id=lang_text_id, paragraph=validated_text, order_num=order_num
            ))
            text += f'{validated_text}\n'
            order_num += 1
    ParagraphOfText.objects.bulk_create(paragraphs_obj)
    return text


def get_sentence_and_words_qty(text):
    sentence_enders_pattern = r'[.!?]|\.'
    sentences = re.split(sentence_enders_pattern, text)
    sentences_qty = len(sentences)
    if sentences_qty > 0 and sentences_qty != 1:
        sentences_qty -= 1
    return sentences_qty, len(text.split()), text


def pop_text_file_qty(paragraph_text, lang_text_id, text_obj_id):
    text = save_text_of_paragraphs(paragraph_text, lang_text_id, text_obj_id)
    return get_sentence_and_words_qty(text)


@shared_task()
def text_validate_and_config_task(obj_id):
    texts = LangText.objects.filter(text_obj_id=obj_id)
    for text in texts:
        if text.text:
            sentences_qty, word_qty, validated_text = pop_text_file_qty(text.text, text.id, obj_id)
            text.word_qty = word_qty
            text.sentence_qty = sentences_qty
            text.text = validated_text
            text.save()
        elif text.file:
            paragraph_text = get_text_from_paragraphs(text.file)
            sentences_qty, word_qty, validated_text = pop_text_file_qty(paragraph_text, text.id, obj_id)
            text.word_qty = word_qty
            text.sentence_qty = sentences_qty
            text.text = paragraph_text
            text.save()
