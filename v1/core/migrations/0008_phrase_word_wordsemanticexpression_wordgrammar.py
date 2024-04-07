# Generated by Django 4.2 on 2024-03-08 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_text_sentence_qty_en_text_word_qty_en'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.phrase')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('word', models.CharField(max_length=255)),
                ('phrase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.phrase')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WordSemanticExpression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('phrase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.phrase')),
                ('word', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='word_semantic_expressions', to='core.word')),
            ],
            options={
                'unique_together': {('word', 'phrase')},
            },
        ),
        migrations.CreateModel(
            name='WordGrammar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('phrase', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.phrase')),
                ('word', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='word_grammars', to='core.word')),
            ],
            options={
                'unique_together': {('word', 'phrase')},
            },
        ),
    ]
