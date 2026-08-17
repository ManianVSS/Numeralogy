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
        'sum',
        'recursive_sum',
        'source_file',
        'uploaded_at',
    )
    search_fields = ('name', 'source_file')
    list_filter = ('uploaded_at', 'source_file')
    readonly_fields = (
        'sum',
        'recursive_sum',
        'uploaded_at',
    )
