# Generated by Django 2.1.5 on 2019-01-19 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lot', '0003_question_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='lot',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
    ]
