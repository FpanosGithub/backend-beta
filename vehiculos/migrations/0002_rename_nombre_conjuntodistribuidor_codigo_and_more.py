# Generated by Django 4.1.3 on 2022-11-30 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingenieria', '0001_initial'),
        ('vehiculos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conjuntodistribuidor',
            old_name='nombre',
            new_name='codigo',
        ),
        migrations.RenameField(
            model_name='conjuntosi',
            old_name='nombre',
            new_name='codigo',
        ),
        migrations.RenameField(
            model_name='elementosi',
            old_name='nombre',
            new_name='codigo',
        ),
        migrations.RemoveField(
            model_name='sistintegradovehiculo',
            name='EEM',
        ),
        migrations.RemoveField(
            model_name='sistintegradovehiculo',
            name='keeper',
        ),
        migrations.RemoveField(
            model_name='sistintegradovehiculo',
            name='marcado',
        ),
        migrations.RemoveField(
            model_name='sistintegradovehiculo',
            name='owner',
        ),
        migrations.AlterField(
            model_name='sistintegradovehiculo',
            name='tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='ingenieria.tiposistemaintegrado'),
        ),
    ]
