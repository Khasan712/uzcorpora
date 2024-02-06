from v1.core.models import Newspaper
import docx
from celery import shared_task


@shared_task()
def pop_text_from_file(source_type, obj_id):
    if source_type == 'newspaper':
        obj = Newspaper.objects.get(id=obj_id)
        paragraphs = docx.Document(obj.file).paragraphs
        text = '\n'.join([para.text for para in paragraphs if para.text])
        obj.text = text
        obj.save()
