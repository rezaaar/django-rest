# Generated by Django 4.2.10 on 2024-04-13 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_alter_answer_type_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='type_result',
            field=models.CharField(max_length=1),
        ),
    ]