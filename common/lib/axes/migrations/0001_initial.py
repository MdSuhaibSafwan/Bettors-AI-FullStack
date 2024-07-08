# Generated by Django 4.2.1 on 2024-01-25 16:33

import common.lib.axes.models
from django.db import migrations, models
import encrypted_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessFailureLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_user_agent', encrypted_fields.fields.EncryptedCharField(max_length=255, verbose_name='User Agent')),
                ('user_agent', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_user_agent', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_ip_address', common.lib.axes.models.EncryptedIPAddressField(null=True, verbose_name='IP Address')),
                ('ip_address', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_ip_address', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_username', encrypted_fields.fields.EncryptedCharField(max_length=255, null=True, verbose_name='Username')),
                ('username', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_username', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_http_accept', encrypted_fields.fields.EncryptedCharField(max_length=1025, verbose_name='HTTP Accept')),
                ('http_accept', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_http_accept', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_path_info', encrypted_fields.fields.EncryptedCharField(max_length=255, verbose_name='Path')),
                ('path_info', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_path_info', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('attempt_time', models.DateTimeField(auto_now_add=True, verbose_name='Attempt Time')),
                ('locked_out', models.BooleanField(blank=True, default=False, verbose_name='Access lock out')),
            ],
            options={
                'verbose_name': '03_AccessFailure',
                'verbose_name_plural': '03_AccessFailure',
            },
        ),
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_user_agent', encrypted_fields.fields.EncryptedCharField(max_length=255, verbose_name='User Agent')),
                ('user_agent', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_user_agent', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_ip_address', common.lib.axes.models.EncryptedIPAddressField(null=True, verbose_name='IP Address')),
                ('ip_address', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_ip_address', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_username', encrypted_fields.fields.EncryptedCharField(max_length=255, null=True, verbose_name='Username')),
                ('username', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_username', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_http_accept', encrypted_fields.fields.EncryptedCharField(max_length=1025, verbose_name='HTTP Accept')),
                ('http_accept', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_http_accept', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_path_info', encrypted_fields.fields.EncryptedCharField(max_length=255, verbose_name='Path')),
                ('path_info', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_path_info', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('attempt_time', models.DateTimeField(auto_now_add=True, verbose_name='Attempt Time')),
                ('logout_time', models.DateTimeField(blank=True, null=True, verbose_name='Logout Time')),
            ],
            options={
                'verbose_name': '02_認証成功ログ',
                'verbose_name_plural': '02_認証成功ログ',
            },
        ),
        migrations.CreateModel(
            name='AccessAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_user_agent', encrypted_fields.fields.EncryptedCharField(max_length=255, verbose_name='User Agent')),
                ('user_agent', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_user_agent', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_ip_address', common.lib.axes.models.EncryptedIPAddressField(null=True, verbose_name='IP Address')),
                ('ip_address', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_ip_address', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_username', encrypted_fields.fields.EncryptedCharField(max_length=255, null=True, verbose_name='Username')),
                ('username', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_username', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_http_accept', encrypted_fields.fields.EncryptedCharField(max_length=1025, verbose_name='HTTP Accept')),
                ('http_accept', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_http_accept', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_path_info', encrypted_fields.fields.EncryptedCharField(max_length=255, verbose_name='Path')),
                ('path_info', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_path_info', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('attempt_time', models.DateTimeField(auto_now_add=True, verbose_name='Attempt Time')),
                ('_get_data', common.lib.axes.models.EncryptedTextField(verbose_name='GET Data')),
                ('get_data', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_get_data', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_post_data', common.lib.axes.models.EncryptedTextField(verbose_name='POST Data')),
                ('post_data', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_get_data', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('failures_since_start', models.PositiveIntegerField(verbose_name='Failed Logins')),
            ],
            options={
                'verbose_name': '01_認証失敗/アカウントロックログ(解除の場合には本ログを削除)',
                'verbose_name_plural': '01_認証失敗/アカウントロックログ(解除の場合には本ログを削除)',
                'unique_together': {('username', 'ip_address', 'user_agent')},
            },
        ),
    ]