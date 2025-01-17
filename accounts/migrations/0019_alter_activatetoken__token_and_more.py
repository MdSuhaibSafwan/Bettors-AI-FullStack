# Generated by Django 4.2.10 on 2024-02-11 20:27

import datetime
from django.db import migrations, models
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_alter_activatetoken__token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activatetoken',
            name='_token',
            field=encrypted_fields.fields.EncryptedTextField(default='0a9c57d513e948c8bd7f9ccaacdc9b63', verbose_name='Token(Encrypted:FormNotUsable)'),
        ),
        migrations.AlterField(
            model_name='activatetoken',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 12, 3, 26, 54, 157943)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='unique_account_id',
            field=models.SlugField(default='73bbeda914ad49ec80a81ce9aeaf4a3a', error_messages={'unique': 'This account name is already in use'}, help_text='Alphabets, numbers, underscore, hyphen up to 32 characters', unique=True, verbose_name='Account name'),
        ),
    ]
