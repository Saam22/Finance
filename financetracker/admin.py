from django.contrib import admin
from financetracker.models import Transaction ,Goal
from import_export.admin import ExportMixin
from import_export import resources

# Register your models here.
class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        fields = ('title', 'amount', 'transaction_type', 'date', 'category')

class TransactionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = TransactionResource
    list_display = ('title', 'user', 'transaction_type', 'amount', 'category', 'date')
    list_filter = ('transaction_type', 'category', 'date')
    search_fields = ('title', 'category', 'user__username')
    ordering = ('-date',)

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Goal)
