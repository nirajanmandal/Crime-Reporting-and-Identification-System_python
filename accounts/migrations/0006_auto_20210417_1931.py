# Generated by Django 2.2.18 on 2021-04-17 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210417_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='assets/img/default-avatar.png', upload_to='citizens/'),
        ),
    ]