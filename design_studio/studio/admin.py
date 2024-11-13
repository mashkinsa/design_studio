from django.contrib import admin
from .models import DesignRequest, Category
class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title',)
    list_editable = ('status',)  # Позволяет редактировать статус прямо в списке
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
# Регистрация моделей в админке
admin.site.register(DesignRequest, DesignRequestAdmin)
admin.site.register(Category, CategoryAdmin)
