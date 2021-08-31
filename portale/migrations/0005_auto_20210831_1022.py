# Generated by Django 3.2.5 on 2021-08-31 08:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portale', '0004_rename_data_notice_data_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='data_lesson',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='officehour',
            name='data_officehour',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
