# Generated by Django 4.1.3 on 2022-11-30 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingenieria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoconjuntoeje',
            name='descripción',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='tipoconjuntosi',
            name='descripción',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='tipoelementoeje',
            name='descripción',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='tipoelementosi',
            name='descripción',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='tiposistemaintegrado',
            name='descripción',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='tipovehiculo',
            name='descripción',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
