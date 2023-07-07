# Generated by Django 3.1.13 on 2021-09-13 07:39
import logging

from django.db import migrations
from core.utils.common import trigram_migration_operations

logger = logging.getLogger(__name__)


def forwards(apps, schema_editor):
    if not schema_editor.connection.vendor.startswith('postgres'):
        logger.info(f'Database vendor: {schema_editor.connection.vendor}')
        logger.info('Skipping migration without attempting to CREATE INDEX')
        return

    schema_editor.execute(
        'create index concurrently tasks_annotations_result_idx2 '
        'on task_completion using gin (cast(result as text) gin_trgm_ops);'
    )


def backwards(apps, schema_editor):
    if not schema_editor.connection.vendor.startswith('postgres'):
        logger.info(f'Database vendor: {schema_editor.connection.vendor}')
        logger.info('Skipping migration without attempting to DROP INDEX')
        return

    schema_editor.execute('drop index tasks_annotations_result_idx2;')
    

class Migration(migrations.Migration):
    atomic = False

    dependencies = [('tasks', '0016_auto_20220414_1408')]

    operations = trigram_migration_operations(migrations.RunPython(forwards, backwards))
