# Generated by Django 2.2.20 on 2021-04-28 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection', '0006_auto_20210423_0329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spottedcitizen',
            name='address',
        ),
        migrations.RemoveField(
            model_name='spottedcitizen',
            name='contact_number',
        ),
        migrations.RemoveField(
            model_name='spottedcitizen',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='spottedcitizen',
            name='nationality',
        ),
        migrations.AddField(
            model_name='spottedcitizen',
            name='location',
            field=models.CharField(max_length=50, null=True),
        ),
    ]