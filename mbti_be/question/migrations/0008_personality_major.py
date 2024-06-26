# Generated by Django 4.2.10 on 2024-05-25 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0007_question_question_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personality',
            fields=[
                ('type', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('major_id', models.AutoField(primary_key=True, serialize=False)),
                ('major_name', models.CharField(max_length=100)),
                ('personality_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.personality')),
            ],
        ),
    ]
