# Generated by Django 4.2.7 on 2023-12-04 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_tbltarjetas_tipotarjeta'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblingresos',
            name='tarjeta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.tbltarjetas'),
        ),
    ]
