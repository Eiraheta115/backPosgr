# Generated by Django 2.0.6 on 2018-10-01 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20180924_0319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='docente',
            old_name='formacion_aca',
            new_name='apellido',
        ),
        migrations.RenameField(
            model_name='docente',
            old_name='fechas_nac',
            new_name='fecha_naci',
        ),
        migrations.RenameField(
            model_name='docente',
            old_name='titulo_pre',
            new_name='nombre',
        ),
        migrations.RenameField(
            model_name='docente',
            old_name='contrasena',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='pasos',
            old_name='id_procedimiento',
            new_name='id_proceimiento',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='apellidos',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='id_user_con',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='nombres',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='t_fijo',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='t_movil',
        ),
        migrations.AddField(
            model_name='aspirante',
            name='aceptado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='aspirante',
            name='nombreuser_aspirante',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='docente',
            name='formacion',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='docente',
            name='movil',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='docente',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='docente',
            name='titulo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='docente',
            name='usuario',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='docente',
            name='dui',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='docente',
            name='email',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='docente',
            name='genero',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='pasos',
            name='descripcion',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='pasos',
            name='orden',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='procedimiento',
            name='descripcion',
            field=models.CharField(max_length=500),
        ),
    ]