# Generated by Django 2.2.18 on 2021-04-17 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210417_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='assets/img/default-avatar.png', upload_to='citizens/'),
        ),
    ]
