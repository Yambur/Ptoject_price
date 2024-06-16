from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Contact)


@admin.action(description="Списание задолженности")
def make_published(request, queryset):
    queryset.update(debt=0)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller_type', 'supplier',)
    list_filter = ('seller_type', 'contact__city',)
    actions = [make_published]

    def contact_city(self, obj):
        return obj.contacts.city
