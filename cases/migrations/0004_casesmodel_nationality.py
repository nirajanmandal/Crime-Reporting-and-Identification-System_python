# Generated by Django 2.2.18 on 2021-04-17 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0003_auto_20201017_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='casesmodel',
            name='nationality',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
