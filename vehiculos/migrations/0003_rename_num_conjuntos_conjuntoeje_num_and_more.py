# Generated by Django 4.1.3 on 2022-11-30 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingenieria', '0002_alter_tipoconjuntoeje_descripción_and_more'),
        ('vehiculos', '0002_rename_nombre_conjuntodistribuidor_codigo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conjuntoeje',
            old_name='num_conjuntos',
            new_name='num',
        ),
        migrations.RenameField(
            model_name='elementoeje',
            old_name='num_elementos',
            new_name='num',
        ),
        migrations.RemoveField(
            model_name='conjuntoeje',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='conjuntosi',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='conjuntosi',
            name='documentacion_tecnica',
        ),
        migrations.RemoveField(
            model_name='elementoeje',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='elementosi',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='elementosi',
            name='documentacion_tecnica',
        ),
        migrations.RemoveField(
            model_name='sistintegradovehiculo',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='sistintegradovehiculo',
            name='documentacion_tecnica',
        ),
        migrations.AlterField(
            model_name='conjuntosi',
            name='tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='ingenieria.tipoconjuntosi'),
        ),
        migrations.AlterField(
            model_name='elementosi',
            name='tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='ingenieria.tipoelementosi'),
        ),
    ]
