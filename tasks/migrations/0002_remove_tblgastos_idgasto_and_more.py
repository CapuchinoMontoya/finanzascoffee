# Generated by Django 4.2.7 on 2023-11-22 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblgastos',
            name='idGasto',
        ),
        migrations.RemoveField(
            model_name='tblingresos',
            name='idIngreso',
        ),
    ]
