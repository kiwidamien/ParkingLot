# Generated by Django 2.1.5 on 2019-01-20 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lot', '0002_auto_20190120_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='starter_name',
            field=models.CharField(default='Anonymous', max_length=100),
        ),
    ]