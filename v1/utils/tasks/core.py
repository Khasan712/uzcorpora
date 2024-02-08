from v1.core.models import Text
import docx
from celery import shared_task


@shared_task()
def pop_text_from_file(obj_id):
    obj = Text.objects.get(id=obj_id)
    paragraphs = docx.Document(obj.file).paragraphs
    text = '\n'.join([para.text for para in paragraphs if para.text])
    obj.text = text
    obj.save()
