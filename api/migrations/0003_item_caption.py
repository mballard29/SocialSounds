# Generated by Django 3.1.2 on 2020-12-03 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201120_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='caption',
            field=models.TextField(blank=True, null=True),
        ),
    ]
