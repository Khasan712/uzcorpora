from django.db.models.signals import post_save
from django.dispatch import receiver
from v1.core.models import Text
from v1.utils.tasks.core import pop_text_from_file, count_words_and_sentences


@receiver(post_save, sender=Text)
def text_signals(sender, instance, created, **kwargs):
    if created:
        if instance.file:
            pop_text_from_file.delay(instance.id)
        elif instance.text:
            count_words_and_sentences.delay(instance.id)

