# Generated by Django 4.2.10 on 2024-02-18 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0010_delete_userproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripePaymentLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_link', models.URLField()),
                ('date_create', models.DateTimeField(auto_now_add=True, help_text='Creation Date and Time', verbose_name='Creation Date and Time')),
                ('user', models.ForeignKey(help_text='Payment Link of a User', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]