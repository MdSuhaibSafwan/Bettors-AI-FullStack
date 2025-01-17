# Generated by Django 4.2.10 on 2024-02-14 21:27

import datetime
from django.db import migrations, models
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_alter_activatetoken__token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activatetoken',
            name='_token',
            field=encrypted_fields.fields.EncryptedTextField(default='4d5c6818b306467b925f41818367384b', verbose_name='Token(Encrypted:FormNotUsable)'),
        ),
        migrations.AlterField(
            model_name='activatetoken',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 15, 4, 26, 59, 912237)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='unique_account_id',
            field=models.SlugField(default='ab977041ba0340f19cd684fc0fe21a1b', error_messages={'unique': 'This account name is already in use'}, help_text='Alphabets, numbers, underscore, hyphen up to 32 characters', unique=True, verbose_name='Account name'),
        ),
    ]
