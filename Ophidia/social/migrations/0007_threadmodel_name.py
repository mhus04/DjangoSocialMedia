# Generated by Django 3.2.8 on 2022-02-18 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_messagemodel_threadmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='threadmodel',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
