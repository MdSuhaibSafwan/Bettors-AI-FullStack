# Generated by Django 4.2.10 on 2024-02-12 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_stripecheckout_raw_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproduct',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userproduct',
            name='stripe_product_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]