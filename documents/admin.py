from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DocumentCategory, FarmDocument


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(FarmDocument)
class FarmDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'document_type', 'category', 'uploaded_by',
        'upload_date', 'expiry_date', 'is_confidential', 'is_expired'
    )
    list_filter = ('document_type', 'category', 'is_confidential', 'upload_date')
    search_fields = ('title', 'description', 'uploaded_by__username')
    readonly_fields = ('upload_date', 'file_extension', 'is_expired')
