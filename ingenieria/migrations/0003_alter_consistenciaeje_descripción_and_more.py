# Generated by Django 4.1.3 on 2022-11-30 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingenieria', '0002_alter_tipoconjuntoeje_descripción_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consistenciaeje',
            name='descripción',
            field=models.CharField(max_length=300, unique=True),
        ),
        migrations.AlterField(
            model_name='consistenciasi',
            name='descripción',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
