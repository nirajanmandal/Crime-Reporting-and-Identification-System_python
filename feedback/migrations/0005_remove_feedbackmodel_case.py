# Generated by Django 2.2.20 on 2021-04-28 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_auto_20210428_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackmodel',
            name='case',
        ),
    ]
