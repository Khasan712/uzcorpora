from v1.core.models import ParagraphOfText, LangText
import docx
import re
from celery import shared_task
from v1.utils.validations import validate_text_apostrophe


def save_paragraph_of_text(paragraphs, lang_text_id, text_obj_id):
    text = ''
    paragraphs_obj = []
    order_num = 1
    for paragraph in paragraphs:
        if paragraph.text:
            validated_text = validate_text_apostrophe(paragraph.text).strip()
            paragraphs_obj.append(ParagraphOfText(
                text_id=text_obj_id, lang_text_id=lang_text_id, paragraph=validated_text, order_num=order_num
            ))
            text += f'{validated_text}\n'
            order_num += 1
    ParagraphOfText.objects.bulk_create(paragraphs_obj)
    return text


def save_text_of_paragraphs(paragraphs: str, lang_text_id, text_obj_id):
    text = ''
    paragraphs_obj = []
    order_num = 1
    for paragraph in paragraphs.splitlines():
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
    return sentences_qty - 1 if sentences_qty > 0 else sentences_qty, len(text.split())


def pop_text_file_qty(text_file, lang_text_id, text_obj_id):
    if isinstance(text_file, str):
        text = save_text_of_paragraphs(text_file, lang_text_id, text_obj_id)
        return get_sentence_and_words_qty(text)
    paragraphs = docx.Document(text_file).paragraphs
    text = save_paragraph_of_text(paragraphs, lang_text_id, text_obj_id)
    return get_sentence_and_words_qty(text)[0], get_sentence_and_words_qty(text)[1], text


@shared_task()
def text_validate_and_config_task(obj_id):
    texts = LangText.objects.filter(text_obj_id=obj_id)
    for text in texts:
        if text.text:
            sentences_qty, word_qty = pop_text_file_qty(text.text, text.id, obj_id)
            text.word_qty = word_qty
            text.sentence_qty = sentences_qty
            text.save()
        elif text.file:
            sentences_qty, word_qty, paragraph_text = pop_text_file_qty(text.file, text.id, obj_id)
            text.word_qty = word_qty
            text.sentence_qty = sentences_qty
            text.text = paragraph_text
            text.save()
