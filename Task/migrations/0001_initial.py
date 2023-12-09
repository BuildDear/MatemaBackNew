# Generated by Django 4.2.6 on 2023-12-01 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('text', models.TextField()),
                ('point', models.IntegerField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='task_photos/')),
                ('answer_matching', models.JSONField(null=True)),
                ('answer_short', models.JSONField(null=True)),
                ('answer_mcq', models.JSONField(null=True)),
            ],
            options={
                'db_table': 'Task',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Theme',
            },
        ),
        migrations.CreateModel(
            name='TypeAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TypeAnswer',
            },
        ),
        migrations.CreateModel(
            name='UserTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task.theme')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'db_table': 'UserTheme',
            },
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_weekly', models.BooleanField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task.task', to_field='name')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'db_table': 'TaskList',
            },
        ),
        migrations.AddField(
            model_name='task',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task.theme'),
        ),
        migrations.AddField(
            model_name='task',
            name='type_ans',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task.typeanswer'),
        ),
        migrations.CreateModel(
            name='DoneTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_done', models.BooleanField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task.task', to_field='name')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'db_table': 'DoneTask',
            },
        ),
    ]
