from django.contrib import admin
from financetracker.models import Transaction ,Goal
# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'transaction_type', 'amount', 'category', 'date')
    list_filter = ('transaction_type', 'category', 'date')
    search_fields = ('title', 'category', 'user__username')
    ordering = ('-date',)

admin.site.register(Goal)
