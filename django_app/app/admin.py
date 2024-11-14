from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Products, OrderDetails, Categories, ProductTags, Cart, ProductCartMapper

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    model = Categories
    list_display = ('id', 'name', 'parent',)
    list_filter = ('name', 'parent',)
    
    search_fields = ('name', 'parent',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    model = Products
    list_display = ('id', 'name', 'image', 'price', 'stock',)
    list_filter = ('name', 'price', 'stock')
    
    search_fields = ('name',)


@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    model = OrderDetails
    list_display = ('id', 'user', 'order_hash', 'order_date',)
    list_filter = ('user', 'order_date',)
    
    search_fields = ('user',)
    ordering = ('-order_date',)


@admin.register(ProductTags)
class ProductTagsAdmin(admin.ModelAdmin):
    model = ProductTags
    list_display = ('id', 'name', 'get_products', )
    list_filter = ('name',)

    search_fields = ('name',)

    def get_products(self, obj):
        return " | ".join([product.name for product in obj.product.all()])
        
    get_products.short_description = 'Tagged Products'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('id', 'user', 'created_on')
    list_filter = ('user', 'created_on')

    search_fields = ('user',)


@admin.register(ProductCartMapper)
class ProductCartMapperAdmin(admin.ModelAdmin):
    model = ProductCartMapper
    list_display = ('id', 'get_cart_details', 'product', 'quantity')
    list_filter = ('cart',)

    search_fields = ('get_cart_details',)

    def get_cart_details(self, obj):
        return str(obj.cart.user.email)+"__"+obj.cart.created_on.strftime("%Y-%m-%d %H:%M:%S")