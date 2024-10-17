# Generated by Django 5.1.1 on 2024-10-16 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FormApp', '0003_memo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('picture', models.FileField(upload_to='picture/%Y/%m/%d')),
            ],
        ),
    ]