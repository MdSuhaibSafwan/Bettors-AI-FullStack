# Generated by Django 5.0.2 on 2024-02-08 18:42

import datetime
import encrypted_fields.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_activatetoken__token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activatetoken',
            name='_token',
            field=encrypted_fields.fields.EncryptedTextField(default='aef0de4ef2a3425e825d8fc2719b69e5', verbose_name='Token(Encrypted:FormNotUsable)'),
        ),
        migrations.AlterField(
            model_name='activatetoken',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 8, 19, 42, 1, 272567)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='unique_account_id',
            field=models.SlugField(default='9d05dee2682b44a7b9c91678ad574b85', error_messages={'unique': 'This account name is already in use'}, help_text='Alphabets, numbers, underscore, hyphen up to 32 characters', unique=True, verbose_name='Account name'),
        ),
    ]