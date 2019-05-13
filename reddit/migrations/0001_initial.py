# Generated by Django 2.2.1 on 2019-05-13 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workspaces', '0003_user_has_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=64)),
                ('subreddit', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=256)),
                ('url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspaces.Channel')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subreddit', models.CharField(max_length=128)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspaces.Channel')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspaces.User')),
            ],
            options={
                'unique_together': {('channel', 'subreddit')},
            },
        ),
    ]
