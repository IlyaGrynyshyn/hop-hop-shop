# Generated by Django 5.0.6 on 2024-07-23 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0009_alter_productattributes_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
