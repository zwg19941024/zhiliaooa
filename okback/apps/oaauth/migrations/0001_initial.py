# Generated by Django 5.1.3 on 2024-12-20 11:03

import apps.oaauth.models
import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=22, max_length=22, prefix='', primary_key=True, serialize=False)),
                ('realname', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telephone', models.CharField(blank=True, max_length=20)),
                ('is_staff', models.BooleanField(default=True)),
                ('status', models.IntegerField(choices=[(1, 'Actived'), (2, 'Unactive'), (3, 'Locked')], default=2)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', apps.oaauth.models.OAUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='OADepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('intro', models.CharField(max_length=200)),
                ('leader', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leader_department', related_query_name='leader_department', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager_departments', related_query_name='manager_departments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='oauser',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staffs', related_query_name='staffs', to='oaauth.oadepartment'),
        ),
    ]