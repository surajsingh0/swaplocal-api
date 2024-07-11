from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description', 'owner__username')
