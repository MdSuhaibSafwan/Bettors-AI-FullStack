# Generated by Django 5.0.1 on 2024-01-27 22:03

import datetime
import encrypted_fields.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_activatetoken__token_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activatetoken',
            options={'verbose_name': '02_Issue Authentication Token', 'verbose_name_plural': '02_Issue Authentication Token'},
        ),
        migrations.AlterField(
            model_name='activatetoken',
            name='_token',
            field=encrypted_fields.fields.EncryptedTextField(default='316456721b1e44b1bdc1846bfc8c4bac', verbose_name='Token(Encrypted:FormNotUsable)'),
        ),
        migrations.AlterField(
            model_name='activatetoken',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 27, 23, 3, 39, 782439)),
        ),
        migrations.AlterField(
            model_name='activatetoken',
            name='token',
            field=encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_token', hash_key='84ef13ba3a0f34e08fdb782f08da11680395c0c3dcc52a558e723629d32fcc27', max_length=66, null=True, unique=True, verbose_name='Token'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='_email',
            field=encrypted_fields.fields.EncryptedEmailField(max_length=255, verbose_name='Email address (Encrypted: Cannot be used in Form)'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='change_email',
            field=encrypted_fields.fields.EncryptedEmailField(default='dummy@mail.com', max_length=255, verbose_name='Desired email address for change (Encrypted: Cannot be used in Form)'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_email', error_messages={'unique': 'This email address is already in use'}, hash_key='84ef13ba3a0f34e08fdb782f08da11680395c0c3dcc52a558e723629d32fcc27', help_text='Email address (Unique, up to 255 characters)', max_length=66, null=True, unique=True, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='If inactive, login will not be possible', verbose_name='Account is active'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='unique_account_id',
            field=models.SlugField(default='b461000a395d48ae8aa3f4286fad146a', error_messages={'unique': 'This account name is already in use'}, help_text='Alphabets, numbers, underscore, hyphen up to 32 characters', unique=True, verbose_name='Account name'),
        ),
    ]
