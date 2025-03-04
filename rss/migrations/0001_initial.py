# Generated by Django 5.1 on 2025-02-23 11:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RssFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('img_url', models.URLField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('public', models.BooleanField(default=True)),
                ('custom', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rss_feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rss.rssfeed')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'rss_feed')},
            },
        ),
    ]
