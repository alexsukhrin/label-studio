from django.db.models import Count, Q, OuterRef

from core.utils.db import SQCount
from tasks.models import Annotation, Task
from core.feature_flags import flag_set


def annotate_task_number(queryset):
    if not flag_set(
        'fflag_fix_back_LSDV_4748_annotate_task_number_14032023_short',
        user='auto',
    ):
        return queryset.annotate(task_number=Count('tasks', distinct=True))
    tasks = Task.objects.filter(project=OuterRef('id')).values_list('id')
    return queryset.annotate(task_number=SQCount(tasks))


def annotate_finished_task_number(queryset):
    if not flag_set(
        'fflag_fix_back_LSDV_4748_annotate_task_number_14032023_short',
        user='auto',
    ):
        return queryset.annotate(finished_task_number=Count('tasks', distinct=True, filter=Q(tasks__is_labeled=True)))
    tasks = Task.objects.filter(project=OuterRef('id'), is_labeled=True).values_list('id')
    return queryset.annotate(finished_task_number=SQCount(tasks))


def annotate_total_predictions_number(queryset):
    return queryset.annotate(total_predictions_number=Count('tasks__predictions', distinct=True))


def annotate_total_annotations_number(queryset):
    if not flag_set(
        'fflag_fix_back_LSDV_961_project_list_09022023_short', user='auto'
    ):
        return queryset.annotate(total_annotations_number=Count(
            'tasks__annotations__id', distinct=True, filter=Q(tasks__annotations__was_cancelled=False)
        ))
    subquery = Annotation.objects.filter(
        Q(project=OuterRef('pk'))
        & Q(was_cancelled=False)
    ).values('id')
    return queryset.annotate(total_annotations_number=SQCount(subquery))


def annotate_num_tasks_with_annotations(queryset):
    if not flag_set(
        'fflag_fix_back_LSDV_961_project_list_09022023_short', user='auto'
    ):
        return queryset.annotate(num_tasks_with_annotations=Count(
            'tasks__id',
            distinct=True,
            filter=Q(tasks__annotations__isnull=False)
            & Q(tasks__annotations__ground_truth=False)
            & Q(tasks__annotations__was_cancelled=False)
            & Q(tasks__annotations__result__isnull=False),
        ))
    subquery = Annotation.objects.filter(
        Q(project=OuterRef('pk'))
        & Q(ground_truth=False)
        & Q(was_cancelled=False)
        & Q(result__isnull=False)
    ).values('task__id').distinct()
    return queryset.annotate(num_tasks_with_annotations=SQCount(subquery))


def annotate_useful_annotation_number(queryset):
    if not flag_set(
        'fflag_fix_back_LSDV_961_project_list_09022023_short', user='auto'
    ):
        return queryset.annotate(useful_annotation_number=Count(
            'tasks__annotations__id',
            distinct=True,
            filter=Q(tasks__annotations__was_cancelled=False)
                   & Q(tasks__annotations__ground_truth=False)
                   & Q(tasks__annotations__result__isnull=False),
        ))
    subquery = Annotation.objects.filter(
        Q(project=OuterRef('pk'))
        & Q(was_cancelled=False)
        & Q(ground_truth=False)
        & Q(result__isnull=False)
    ).values('id')
    return queryset.annotate(useful_annotation_number=SQCount(subquery))


def annotate_ground_truth_number(queryset):
    if not flag_set(
        'fflag_fix_back_LSDV_961_project_list_09022023_short', user='auto'
    ):
        return queryset.annotate(ground_truth_number=Count(
            'tasks__annotations__id', distinct=True, filter=Q(tasks__annotations__ground_truth=True)
        ))
    subquery = Annotation.objects.filter(
        Q(project=OuterRef('pk'))
        & Q(ground_truth=True)
    ).values('id')
    return queryset.annotate(ground_truth_number=SQCount(subquery))


def annotate_skipped_annotations_number(queryset):
    if not flag_set(
        'fflag_fix_back_LSDV_961_project_list_09022023_short', user='auto'
    ):
        return queryset.annotate(skipped_annotations_number=Count(
            'tasks__annotations__id', distinct=True, filter=Q(tasks__annotations__was_cancelled=True)
        ))
    subquery = Annotation.objects.filter(
        Q(project=OuterRef('pk'))
        & Q(was_cancelled=True)
    ).values('id')
    return queryset.annotate(skipped_annotations_number=SQCount(subquery))

