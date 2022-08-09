# Generated by Django 4.0.6 on 2022-08-02 04:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketApp', '0008_compra_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle',
            name='compra',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='factura', to='marketApp.compra'),
        ),
        migrations.RemoveField(
            model_name='detalle',
            name='producto',
        ),
        migrations.AddField(
            model_name='detalle',
            name='producto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='producto', to='marketApp.producto'),
        ),
    ]
