# Generated by Django 2.0.6 on 2019-01-15 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0025_auto_20190112_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='arancel',
            name='codigo',
            field=models.CharField(default='n', max_length=10),
            preserve_default=False,
        ),
    ]
