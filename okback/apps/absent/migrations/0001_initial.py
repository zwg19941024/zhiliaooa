# Generated by Django 5.1.3 on 2025-01-01 20:03

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
            name='AbsentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('creata_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Absent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('request_content', models.TextField()),
                ('status', models.IntegerField(choices=[(1, 'Auditing'), (2, 'Pass'), (3, 'Reject')], default=1)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('response_content', models.TextField(blank=True)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='req_absents', related_query_name='req_absents', to=settings.AUTH_USER_MODEL)),
                ('responder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resp_absents', related_query_name='resp_absents', to=settings.AUTH_USER_MODEL)),
                ('absent_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='absents', related_query_name='absents', to='absent.absenttype')),
            ],
        ),
    ]