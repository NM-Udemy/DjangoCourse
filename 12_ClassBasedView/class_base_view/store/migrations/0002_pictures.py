# Generated by Django 5.1.1 on 2024-12-02 02:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('picture', models.FileField(upload_to='pictures/')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='store.books')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
