# Generated by Django 4.2.10 on 2024-02-12 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_remove_userproduct_user_userproduct_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproduct',
            name='name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
