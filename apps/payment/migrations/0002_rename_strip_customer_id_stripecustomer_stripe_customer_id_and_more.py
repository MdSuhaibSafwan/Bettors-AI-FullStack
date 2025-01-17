# Generated by Django 4.2.10 on 2024-02-09 21:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stripecustomer',
            old_name='strip_customer_id',
            new_name='stripe_customer_id',
        ),
        migrations.AlterField(
            model_name='stripecustomer',
            name='stripe_subscription_id',
            field=models.CharField(help_text='Subscription id of user', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='stripecustomer',
            name='user',
            field=models.ForeignKey(help_text='User for Stripe Checkout', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
