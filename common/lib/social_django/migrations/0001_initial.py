# Generated by Django 4.2.1 on 2024-01-25 16:35

import common.lib.social_django.models
import common.lib.social_django.storage
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import encrypted_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Partial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(db_index=True, max_length=32)),
                ('next_step', models.PositiveSmallIntegerField(default=0)),
                ('backend', models.CharField(max_length=32)),
                ('data', models.JSONField(default=dict)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'db_table': 'social_auth_partial',
            },
            bases=(models.Model, common.lib.social_django.storage.DjangoPartialMixin),
        ),
        migrations.CreateModel(
            name='Nonce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_url', models.CharField(max_length=255)),
                ('timestamp', models.IntegerField()),
                ('salt', models.CharField(max_length=65)),
            ],
            options={
                'verbose_name': '02_Nonce',
                'verbose_name_plural': '02_Nonce',
                'db_table': 'social_auth_nonce',
                'unique_together': {('server_url', 'timestamp', 'salt')},
            },
            bases=(models.Model, common.lib.social_django.storage.DjangoNonceMixin),
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('code', models.CharField(db_index=True, max_length=32)),
                ('verified', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'db_table': 'social_auth_code',
                'unique_together': {('email', 'code')},
            },
            bases=(models.Model, common.lib.social_django.storage.DjangoCodeMixin),
        ),
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_url', models.CharField(max_length=255)),
                ('handle', models.CharField(max_length=255)),
                ('secret', models.CharField(max_length=255)),
                ('issued', models.IntegerField()),
                ('lifetime', models.IntegerField()),
                ('assoc_type', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': '03_Association',
                'verbose_name_plural': '03_Association',
                'db_table': 'social_auth_association',
                'unique_together': {('server_url', 'handle')},
            },
            bases=(models.Model, common.lib.social_django.storage.DjangoAssociationMixin),
        ),
        migrations.CreateModel(
            name='UserSocialAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=32)),
                ('_uid', encrypted_fields.fields.EncryptedCharField(max_length=255)),
                ('uid', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_uid', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('_extra_data', common.lib.social_django.models.EncryptedJSONField(default=dict)),
                ('extra_data', encrypted_fields.fields.SearchField(blank=True, db_index=True, encrypted_field_name='_extra_data', hash_key='***YOUR_ENCRYPTION_HASH_KEY***', max_length=66, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_auth', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '01_UserSocialAuth',
                'verbose_name_plural': '01_UserSocialAuth',
                'db_table': 'social_auth_usersocialauth',
                'unique_together': {('provider', 'uid')},
            },
            bases=(models.Model, common.lib.social_django.storage.DjangoUserMixin),
        ),
    ]
