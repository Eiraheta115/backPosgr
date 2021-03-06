# Generated by Django 2.0.6 on 2018-12-10 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_descuento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catergoria',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.Catergoria')),
            ],
        ),
        migrations.CreateModel(
            name='Clasificacion',
            fields=[
                ('id_clasificacion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id_documento', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('entregado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Encuentas',
            fields=[
                ('id_encuensta', models.AutoField(primary_key=True, serialize=False)),
                ('objetivo', models.CharField(max_length=1000)),
                ('instrucciones', models.CharField(max_length=15000)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('id_docente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.Docente')),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id_pregunta', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.Clasificacion')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id_respuesta', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.IntegerField()),
                ('comentario', models.CharField(max_length=750)),
                ('id_encuesta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.Encuentas')),
                ('id_estudiante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.Aspirante')),
                ('id_pregunta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.Pregunta')),
            ],
        ),
    ]
