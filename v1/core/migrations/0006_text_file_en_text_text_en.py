# Generated by Django 4.2 on 2024-02-17 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_text_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='file_en',
            field=models.FileField(blank=True, null=True, upload_to='core/'),
        ),
        migrations.AddField(
            model_name='text',
            name='text_en',
            field=models.TextField(blank=True, null=True, verbose_name='Matn English'),
        ),
    ]
