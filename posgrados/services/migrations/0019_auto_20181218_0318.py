# Generated by Django 2.0.6 on 2018-12-18 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0018_inscripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupoteorico',
            name='D',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grupoteorico',
            name='J',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grupoteorico',
            name='L',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grupoteorico',
            name='M',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grupoteorico',
            name='S',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grupoteorico',
            name='V',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grupoteorico',
            name='X',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]