# Generated by Django 4.2.7 on 2023-11-14 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_order_completed_order_delivredat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.order'),
        ),
    ]
