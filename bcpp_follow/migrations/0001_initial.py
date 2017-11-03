# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-13 13:16
from __future__ import unicode_literals

import _socket
from django.db import migrations, models
import django_revision.revision_field
import edc_base.model_fields.hostname_modification_field
import edc_base.model_fields.userfield
import edc_base.model_fields.uuid_auto_field
import edc_base.model_validators.date
import edc_base.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WorkList',
            fields=[
                ('created', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('modified', models.DateTimeField(blank=True, default=edc_base.utils.get_utcnow)),
                ('user_created', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user created')),
                ('user_modified', edc_base.model_fields.userfield.UserField(blank=True, help_text='Updated by admin.save_model', max_length=50, verbose_name='user modified')),
                ('hostname_created', models.CharField(blank=True, default=_socket.gethostname, help_text='System field. (modified on create only)', max_length=60)),
                ('hostname_modified', edc_base.model_fields.hostname_modification_field.HostnameModificationField(blank=True, help_text='System field. (modified on every save)', max_length=50)),
                ('revision', django_revision.revision_field.RevisionField(blank=True, editable=False, help_text='System field. Git repository tag:branch:commit.', max_length=75, null=True, verbose_name='Revision')),
                ('device_created', models.CharField(blank=True, max_length=10)),
                ('device_modified', models.CharField(blank=True, max_length=10)),
                ('id', edc_base.model_fields.uuid_auto_field.UUIDAutoField(blank=True, editable=False, help_text='System auto field. UUID primary key.', primary_key=True, serialize=False)),
                ('slug', models.CharField(db_index=True, default='', editable=False, help_text='a field used for quick search', max_length=250, null=True)),
                ('subject_identifier', models.CharField(max_length=50, verbose_name='Subject Identifier')),
                ('report_datetime', models.DateTimeField(null=True, validators=[edc_base.model_validators.date.datetime_not_future], verbose_name='Correction report date ad time')),
                ('map_area', models.CharField(max_length=25)),
                ('is_called', models.BooleanField(default=False, editable=False)),
                ('called_datetime', models.DateTimeField(editable=False, null=True)),
                ('visited', models.CharField(editable=False, max_length=25, null=True)),
            ],
        ),
    ]
