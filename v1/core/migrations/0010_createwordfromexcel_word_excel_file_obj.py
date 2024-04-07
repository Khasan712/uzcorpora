# Generated by Django 4.2 on 2024-03-08 19:35

from django.db import migrations, models
import django.db.models.deletion
import v1.utils.validations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_word_lemma'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateWordFromExcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('word_phrase', models.CharField(choices=[('grammar', 'grammar'), ('semantic_expression', 'semantic_expression')], max_length=50)),
                ('file', models.FileField(upload_to='create_word_from_file/', validators=[v1.utils.validations.validate_file_format_excel])),
                ('phrase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.phrase')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='word',
            name='excel_file_obj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_obj', to='core.createwordfromexcel'),
        ),
    ]
