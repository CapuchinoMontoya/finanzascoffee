# Generated by Django 4.2.7 on 2023-11-30 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0002_remove_tblgastos_idgasto_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblTarjetas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreTarjeta', models.TextField(blank=True)),
                ('cantidadDisponible', models.BigIntegerField()),
                ('tipoTarjeta', models.TextField()),
                ('fechaPago', models.DateField(null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]