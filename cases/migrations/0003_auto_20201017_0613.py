# Generated by Django 2.2.16 on 2020-10-17 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_auto_20201017_0556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casesmodel',
            name='status',
            field=models.CharField(choices=[('Wanted', 'Wanted'), ('Spotted', 'Spotted'), ('Missing', 'Missing'), ('Found', 'Found')], default='free', max_length=10),
            preserve_default=False,
        ),
    ]
