# Generated by Django 4.1.3 on 2022-11-30 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculos', '0003_rename_num_conjuntos_conjuntoeje_num_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distribuidor',
            name='EEM',
        ),
        migrations.RemoveField(
            model_name='distribuidor',
            name='documentacion_tecnica',
        ),
        migrations.RemoveField(
            model_name='distribuidor',
            name='imagen',
        ),
        migrations.RemoveField(
            model_name='distribuidor',
            name='keeper',
        ),
        migrations.RemoveField(
            model_name='distribuidor',
            name='marcado',
        ),
        migrations.RemoveField(
            model_name='distribuidor',
            name='owner',
        ),
    ]
