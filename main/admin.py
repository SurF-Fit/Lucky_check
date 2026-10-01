from django.contrib import admin
from .models import Receipt, Profile


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'fn', 'fd', 'fp', 'amount', 'status', 'purchased_at', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('fn', 'fd', 'fp', 'user__username')
    readonly_fields = ('created_at',)
    list_editable = ('status',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')