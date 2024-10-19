# Generated by Django 4.1 on 2024-10-18 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_remove_quote_end_day_remove_quote_end_month_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quote",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.category",
            ),
        ),
    ]
