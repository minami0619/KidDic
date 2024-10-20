# Generated by Django 4.1 on 2024-10-20 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_user_is_first_login"),
    ]

    operations = [
        migrations.AlterField(
            model_name="family",
            name="invite_url",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="family",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="members",
                to="app.family",
            ),
        ),
    ]
