# Generated by Django 4.1.3 on 2022-11-30 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingenieria', '0003_alter_consistenciaeje_descripción_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='consistenciaeje',
            name='unidades_medida',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='consistenciasi',
            name='unidades_medida',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
