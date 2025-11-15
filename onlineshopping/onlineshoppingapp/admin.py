from django.contrib import admin
from .models import Product, Category, Wishlist, Cart

# Customize Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'description')
    list_filter = ('category', 'price')
    search_fields = ('name', 'description')
    list_editable = ('price',)
    list_per_page = 20
    ordering = ('-id',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Pricing & Category', {
            'fields': ('price', 'category')
        }),
        ('Product Image', {
            'fields': ('image',)
        }),
    )
    
    # Allow admin to edit, view, and delete
    def has_module_permission(self, request):
        return request.user.is_staff
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
    
    def has_add_permission(self, request):
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff


# Customize Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_per_page = 20
    ordering = ('name',)
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description', 'image')
        }),
    )
    
    # Allow admin to edit, view, and delete
    def has_module_permission(self, request):
        return request.user.is_staff
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
    
    def has_add_permission(self, request):
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff


# Customize Wishlist Admin
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_on')
    list_filter = ('added_on',)
    search_fields = ('user__username', 'product__name')
    ordering = ('-added_on',)


# Customize Cart Admin
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_on', 'get_total_price')
    list_filter = ('added_on',)
    search_fields = ('user__username', 'product__name')
    ordering = ('-added_on',)


# Register models with custom admin classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Cart, CartAdmin)

# Customize admin site headers
admin.site.site_header = "Online Shopping Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Online Shopping Administration"
