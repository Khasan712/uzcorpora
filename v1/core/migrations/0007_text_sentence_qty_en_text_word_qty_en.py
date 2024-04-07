# Generated by Django 4.2 on 2024-02-17 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_text_file_en_text_text_en'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='sentence_qty_en',
            field=models.PositiveIntegerField(default=0, verbose_name='Gap miqdori English'),
        ),
        migrations.AddField(
            model_name='text',
            name='word_qty_en',
            field=models.PositiveIntegerField(default=0, verbose_name="So'z miqdori English"),
        ),
    ]
