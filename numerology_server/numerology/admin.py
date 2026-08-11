from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import NameEntry


class NameEntryResource(resources.ModelResource):
    class Meta:
        model = NameEntry
        fields = (
            'id',
            'name',
            'initial',
            'full_name',
            'sum_without_initial',
            'recursive_sum_without_initial',
            'sum',
            'recursive_sum',
            'source_file',
            'uploaded_at',
        )


@admin.register(NameEntry)
class NameEntryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = NameEntryResource
    list_display = (
        'name',
        'initial',
        'full_name',
        'sum_without_initial',
        'recursive_sum_without_initial',
        'sum',
        'recursive_sum',
        'source_file',
        'uploaded_at',
    )
    search_fields = ('name', 'initial', 'full_name', 'source_file')
    list_filter = ('uploaded_at', 'source_file')
    readonly_fields = (
        'sum_without_initial',
        'recursive_sum_without_initial',
        'sum',
        'recursive_sum',
        'full_name',
        'uploaded_at',
    )
