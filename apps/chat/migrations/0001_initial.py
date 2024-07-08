# Generated by Django 4.2.1 on 2024-01-25 16:35

import apps.chat.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.SlugField(default='863232cbfa524c6d8681e01648ae01de', unique=True, verbose_name='ルームID')),
                ('date_create', models.DateTimeField(default=django.utils.timezone.now, help_text='作成日時', verbose_name='作成日時')),
                ('create_user', models.ForeignKey(help_text='紐づくアカウントID', on_delete=django.db.models.deletion.CASCADE, related_name='related_room_model_create_user', to=settings.AUTH_USER_MODEL, verbose_name='作成者')),
            ],
            options={
                'verbose_name': 'ルーム一覧',
                'verbose_name_plural': 'ルーム一覧',
                'db_table': 'room_model',
            },
        ),
        migrations.CreateModel(
            name='RoomSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(default='NewChatRoom', help_text='半角英数字 50文字以下', max_length=50, verbose_name='ルーム名')),
                ('ai_icon', models.ImageField(default='..//static//apps/chat/ai_icon/default/ai.png', help_text='画像は 400(px)x400(px) にリサイズされます', upload_to=apps.chat.models.get_ai_icon_image_path, verbose_name='AIアイコン')),
                ('system_sentence', models.TextField(blank=True, default='', help_text='最大1500文字', max_length=1500, null=True, verbose_name='システムメッセージ')),
                ('assistant_sentence', models.TextField(blank=True, default='', help_text='最大1500文字', max_length=1500, null=True, verbose_name='アシスタントメッセージ')),
                ('history_len', models.IntegerField(default=0, help_text='ヒストリーに含める直近の会話数(最大30)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(30)], verbose_name='history_len')),
                ('max_tokens', models.IntegerField(default=256, help_text='生成されるトークンの最大長(最大2048)', validators=[django.core.validators.MinValueValidator(50), django.core.validators.MaxValueValidator(2048)], verbose_name='max_tokens')),
                ('temperature', models.FloatField(default=1.0, help_text='生成するテキストのランダム性(between 0 and 2)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)], verbose_name='temperature')),
                ('top_p', models.FloatField(default=1.0, help_text='単語の選択性(between 0 and 1)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='top_p')),
                ('presence_penalty', models.FloatField(default=1.0, help_text='既出単語への一定ペナルティ(between -2 and 2)', validators=[django.core.validators.MinValueValidator(-2), django.core.validators.MaxValueValidator(2)], verbose_name='presence_penalty')),
                ('frequency_penalty', models.FloatField(default=1.0, help_text='既出単語の出現回数へのペナルティ(between -2 and 2)', validators=[django.core.validators.MinValueValidator(-2), django.core.validators.MaxValueValidator(2)], verbose_name='frequency_penalty')),
                ('comment', models.TextField(blank=True, default='', help_text='半角英数字 256文字以下', max_length=256, null=True, verbose_name='コメント/メモ')),
                ('room_id', models.OneToOneField(help_text='紐づくルームID', on_delete=django.db.models.deletion.CASCADE, related_name='related_room_settings_model_room_id', to='chat.room', verbose_name='ルームID')),
            ],
            options={
                'verbose_name': 'ルーム設定',
                'verbose_name_plural': 'ルーム設定',
                'db_table': 'room_settings_model',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_message', models.TextField(blank=True, null=True, verbose_name='ユーザメッセージ')),
                ('user_settings', models.TextField(blank=True, null=True, verbose_name='ユーザのLLM設定')),
                ('llm_response', models.TextField(blank=True, null=True, verbose_name='LLM回答')),
                ('response_info', models.TextField(blank=True, null=True, verbose_name='追加情報')),
                ('date_create', models.DateTimeField(default=django.utils.timezone.now, help_text='作成日時', verbose_name='作成日時')),
                ('room_id', models.ForeignKey(help_text='紐づくルームID', on_delete=django.db.models.deletion.CASCADE, related_name='related_message_model_room_id', to='chat.room', verbose_name='ルームID')),
            ],
            options={
                'verbose_name': 'メッセージ一覧',
                'verbose_name_plural': 'メッセージ一覧',
                'db_table': 'message_model',
            },
        ),
    ]
