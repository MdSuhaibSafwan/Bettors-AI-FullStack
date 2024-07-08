# Generated by Django 4.2.10 on 2024-02-09 10:36

import datetime
from django.db import migrations, models
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_activatetoken__token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activatetoken',
            name='_token',
            field=encrypted_fields.fields.EncryptedTextField(default='a07ebe05282545c8a573e0d0343b524b', verbose_name='Token(Encrypted:FormNotUsable)'),
        ),
        migrations.AlterField(
            model_name='activatetoken',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 9, 17, 36, 10, 348399)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='unique_account_id',
            field=models.SlugField(default='f63ce8704a314a258c8ab33cd310083c', error_messages={'unique': 'This account name is already in use'}, help_text='Alphabets, numbers, underscore, hyphen up to 32 characters', unique=True, verbose_name='Account name'),
        ),
    ]