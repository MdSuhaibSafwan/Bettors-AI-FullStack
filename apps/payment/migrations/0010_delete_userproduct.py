# Generated by Django 4.2.10 on 2024-02-13 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_alter_stripecheckout_raw_data'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProduct',
        ),
    ]
