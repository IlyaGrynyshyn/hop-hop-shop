# Generated by Django 5.0.6 on 2024-09-12 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0003_order_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_type",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
