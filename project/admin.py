from django.contrib import admin
from .models import Record, Product, Customer

class RecordAdmin(admin.ModelAdmin):
    # Display fields from the related Customer model
    list_display = ('get_first_name', 'get_last_name', 'get_email', 'get_phone', 'product', 'get_Id_no', 'Serial_no', 'created_at')
    
    # Make created_at read-only in the admin detail view
    readonly_fields = ('created_at',)

    # Define methods to access related Customer fields
    def get_first_name(self, obj):
        return obj.customer.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.customer.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.customer.email
    get_email.short_description = 'Email'

    def get_phone(self, obj):
        return obj.customer.phone
    get_phone.short_description = 'Phone'

    def get_Id_no(self, obj):
        return obj.customer.Id_no
    get_Id_no.short_description = 'ID No'

# Register the models with the custom admin configuration
admin.site.register(Record, RecordAdmin)
admin.site.register(Product)
admin.site.register(Customer)
