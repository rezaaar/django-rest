# Generated by Django 4.2.10 on 2024-05-26 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_personality_major'),
    ]

    operations = [
        migrations.RenameField(
            model_name='major',
            old_name='personality_type',
            new_name='type',
        ),
    ]