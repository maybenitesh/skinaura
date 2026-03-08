from django.contrib import admin
from .models import Product,Order,OrderItem
from .models import Contact

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'email', 'total_amount', 'created_at')
    list_filter = ('status',)
    inlines = [OrderItemInline]


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)

admin.site.register(Contact)

