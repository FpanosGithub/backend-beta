# Generated by Django 4.1.3 on 2022-12-18 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculos', '0004_remove_distribuidor_eem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiculo',
            name='codigo',
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='matricula',
            field=models.CharField(blank=True, default=' ', max_length=20, null=True, unique=True),
        ),
    ]
