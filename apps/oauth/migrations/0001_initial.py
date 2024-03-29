# Generated by Django 2.2 on 2019-04-23 07:28

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('gid', models.AutoField(db_column='gid', primary_key=True, serialize=False)),
                ('create_or_delete', models.BooleanField(db_column='create_or_delete', default=False)),
                ('update', models.BooleanField(db_column='update', default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GroupUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(db_column='uid')),
                ('gid', models.IntegerField(db_column='gid')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uid', models.AutoField(db_column='uid', max_length=10, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(db_column='username', max_length=150, unique=True)),
                ('password', models.CharField(db_column='password', max_length=150)),
                ('name', models.CharField(blank=True, db_column='name', max_length=150, null=True)),
                ('is_active', models.BooleanField(db_column='is_active', default=True)),
                ('admin', models.BooleanField(db_column='is_admin', default=False)),
                ('developer', models.BooleanField(db_column='is_developer', default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'db_table': 'User',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
