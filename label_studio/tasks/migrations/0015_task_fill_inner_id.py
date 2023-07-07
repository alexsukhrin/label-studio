"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import logging

from django.db import migrations
from django.db.models import F, Window
from django.db.models.functions import RowNumber
from django.db.utils import NotSupportedError
from core.bulk_update_utils import bulk_update
from core.feature_flags import flag_set
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger(__name__)


def remove(apps, schema_editor):
    # if not flag_set('ff_back_2070_inner_id_12052022_short', user=AnonymousUser()):
    return  # we don't want to apply this migration to all projects


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0014_task_inner_id'),
    ]

    operations = [
        migrations.RunPython(remove, backwards),
    ]