from django.contrib import admin
from .models import Exchange

@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'initiator', 'receiver', 'item_offered', 'item_requested', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('initiator__username', 'receiver__username', 'item_offered__title', 'item_requested__title')

