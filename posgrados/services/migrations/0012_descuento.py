# Generated by Django 2.0.6 on 2018-12-10 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_remove_materia_id_user_para'),
    ]

    operations = [
        migrations.CreateModel(
            name='descuento',
            fields=[
                ('id_descuento', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=256, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=1024, null=True)),
                ('activo', models.BooleanField()),
            ],
        ),
    ]
