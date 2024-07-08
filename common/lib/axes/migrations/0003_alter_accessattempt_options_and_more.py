# Generated by Django 5.0.1 on 2024-01-27 22:24

import encrypted_fields.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axes', '0002_alter_accessattempt_get_data_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accessattempt',
            options={'verbose_name': '01_Authentication Failures/Account Lock Logs (Delete this log when unlocking)', 'verbose_name_plural': '01_Authentication Failures/Account Lock Logs (Delete this log when unlocking)'},
        ),
        migrations.AlterModelOptions(
            name='accessfailurelog',
            options={'verbose_name': '03_Access Failure', 'verbose_name_plural': '03_Access Failure'},
        ),
        migrations.AlterModelOptions(
            name='accesslog',
            options={'verbose_name': '02_Successful Authentication Logs', 'verbose_name_plural': '02_Successful Authentication Logs'},
        ),
        migrations.AlterField(
            model_name='accessattempt',
            name='post_data',
            field=encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_post_data', hash_key='84ef13ba3a0f34e08fdb782f08da11680395c0c3dcc52a558e723629d32fcc27', max_length=66, null=True),
        ),
        migrations.AlterField(
            model_name='accessfailurelog',
            name='locked_out',
            field=models.BooleanField(blank=True, default=False, verbose_name='Access Lockout'),
        ),
    ]