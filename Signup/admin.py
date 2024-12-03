from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
        
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Personal Info', {'fields': (
            'first_name', 
            'last_name', 
            'weight', 
            'height', 
            'age',
            'gender',
            'body_goal',
            'intensity',
            'profile_photo'
        )}),
        ('Contact Info', {'fields': (
            'phone_number', 
            'country', 
            'city', 
            'street', 
            'zip_code'
        )})
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'password1', 
                'password2', 
                'is_staff', 
                'is_active'
            )
        }),
    )
    
    search_fields = ['email']
    ordering = ['email']
    
    filter_horizontal = ('groups', 'user_permissions')
    
    # Remove filter_horizontal if not using groups and user_permissions
    # If you want to add these, you'll need to modify your CustomUser model

admin.site.register(CustomUser, CustomUserAdmin)