# Generated by Django 2.0 on 2021-01-06 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0006_auto_20210106_1523'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='YesOrNo',
            new_name='YesOrNoQuestion',
        ),
    ]
