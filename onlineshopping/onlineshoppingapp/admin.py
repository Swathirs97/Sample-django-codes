from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Wishlist, Cart
from .models import Review

# Inline review editing in Product admin
class ReviewInline(admin.TabularInline):
    model = Review
    fields = ('user', 'display_rating', 'comment', 'admin_reply', 'created_at')
    readonly_fields = ('user', 'display_rating', 'comment', 'created_at')
    extra = 0

    def display_rating(self, obj):
        # render rating as star icons (★ filled, ☆ empty)
        if obj is None or obj.rating is None:
            return ''
        try:
            filled = int(round(obj.rating))
        except Exception:
            filled = 0
        filled = max(0, min(5, filled))
        stars = '★' * filled + '☆' * (5 - filled)
        return format_html('<span style="color: #f5c518; font-size: 1.1em;">{}</span>', stars)
    display_rating.short_description = 'Rating'

# Customize Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'description', 'avg_rating', 'reviews_total')
    # show aggregate rating and reviews count in admin list view
    def avg_rating(self, obj):
        return obj.average_rating()
    avg_rating.short_description = 'Avg Rating'

    def reviews_total(self, obj):
        return obj.review_count()
    reviews_total.short_description = 'Reviews'

    list_display = ('name', 'category', 'price', 'description', 'avg_rating', 'reviews_total')
    list_filter = ('category', 'price')
    search_fields = ('name', 'description')
    list_editable = ('price',)
    list_per_page = 20
    ordering = ('-id',)
    inlines = [ReviewInline]
    
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

# Custom Review admin so admins can view replies and respond
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'display_rating', 'comment', 'admin_reply', 'created_at')
    readonly_fields = ('user', 'display_rating', 'comment', 'created_at')
    list_filter = ('created_at', 'product')
    search_fields = ('user__username', 'product__name', 'comment')
    ordering = ('-created_at',)

    def display_rating(self, obj):
        if obj is None or obj.rating is None:
            return ''
        try:
            filled = int(round(obj.rating))
        except Exception:
            filled = 0
        filled = max(0, min(5, filled))
        stars = '★' * filled + '☆' * (5 - filled)
        return format_html('<span style="color: #f5c518; font-size: 1.1em;">{}</span>', stars)
    display_rating.short_description = 'Rating'

# Register Review with the custom admin
admin.site.register(Review, ReviewAdmin)

# Customize admin site headers
admin.site.site_header = "Online Shopping Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Online Shopping Administration"
