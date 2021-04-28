# Generated by Django 2.2.20 on 2021-04-28 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0001_initial'),
        ('feedback', '0003_auto_20210428_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackmodel',
            name='case',
        ),
        migrations.AddField(
            model_name='feedbackmodel',
            name='case',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.CasesModel'),
        ),
    ]
