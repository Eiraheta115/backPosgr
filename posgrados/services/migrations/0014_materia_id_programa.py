# Generated by Django 2.0.6 on 2018-12-16 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0013_catergoria_clasificacion_documento_encuentas_pregunta_respuesta'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='id_programa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.Programa'),
        ),
    ]
