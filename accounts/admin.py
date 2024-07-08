from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import ActivateToken
from .forms import AdminCustomUserCreationForm

User = get_user_model()

class CustomUserAdmin(UserAdmin):

    # List screen
    list_display_ = ('unique_account_id',
                     'email',
                     'change_email',
                     'is_change_email_request',
                     'is_social_login',
                     'is_set_password',
                     'is_active',
                     'is_staff',
                     'is_superuser',
                     'date_create',)
    list_filter   = ['is_change_email_request',
                     'is_social_login',
                     'is_set_password',
                     'is_active',
                     'is_staff',
                     'is_superuser',
                     'date_create',]
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ('unique_account_id',)
    ordering           = ('-date_create',)
    
    # Date drill down menu
    date_hierarchy = 'date_create'
    
    # Display number settings
    list_per_page     = 500
    list_max_show_all = 10000

    # Permission settings
    # Limit to is_superuser by setting CRUD to True (revoke is_staff permissions)
    add_form = AdminCustomUserCreationForm
    add_fieldsets = (
        ('Account Information', {'fields': (
            'unique_account_id',
            'email',
            'password',
            'confirm_password',
            )}),
    )

    # Edit screen
    fieldsets = (
        ('User Information', {'fields': (
            'unique_account_id',
            'email',
            'is_change_email_request',
            )}),
        ('Authentication Information', {'fields': (
            'password',
            'change_email',
            'is_set_password',
            'is_social_login',
            'is_active',
            )}),
        ('Permission Information (Be careful when setting administrator permissions)', {'fields': (
            'is_staff',
            'is_superuser',
            )}),
        ('Others', {'fields': (
            'date_create',
            )}),
    )
    # Permission settings
    # Limit to is_superuser by setting CRUD to True (revoke is_staff permissions)
    is_only_superuser_Create = True
    is_only_superuser_Read   = True
    is_only_superuser_Update = True
    is_only_superuser_Delete = True
    
    if is_only_superuser_Create:
        def has_add_permission(self, request) -> bool:
            return request.user.is_superuser
    else:
        def has_add_permission(self, request) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Read:
        def has_module_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
        def has_view_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_module_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
        def has_view_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Update:
        def has_change_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_change_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Delete:
        def has_delete_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_delete_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff

class ActivateTokenAdmin(admin.ModelAdmin):

    # List screen
    list_display_ = ('user',
                        'token',
                        'expired_at',)
    list_filter   = ['expired_at',]
    list_display       = list_display_
    list_display_links = list_display_
    search_fields      = ()
    ordering           = ('-expired_at',)
    
    # Date drill down menu
    date_hierarchy = 'expired_at'
    
    # Display number settings
    list_per_page     = 500
    list_max_show_all = 10000
    
    # Creation screen
    add_form      = None
    add_fieldsets = None
    
    # Edit screen
    fieldsets = (
        ('Issued Token', {'fields': (
            'user',
            'token',
            'expired_at',
            )}),
    )

    # Permission settings
    # Limit to is_superuser by setting CRUD to True (revoke is_staff permissions)
    is_only_superuser_Create = True
    is_only_superuser_Read   = True
    is_only_superuser_Update = True
    is_only_superuser_Delete = True
    
    if is_only_superuser_Create:
        def has_add_permission(self, request) -> bool:
            return request.user.is_superuser
    else:
        def has_add_permission(self, request) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Read:
        def has_module_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
        def has_view_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_module_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
        def has_view_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Update:
        def has_change_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_change_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff
    if is_only_superuser_Delete:
        def has_delete_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser
    else:
        def has_delete_permission(self, request, obj=None) -> bool:
            return request.user.is_superuser or request.user.is_staff

admin.site.register(User,          CustomUserAdmin)
admin.site.register(ActivateToken, ActivateTokenAdmin)
admin.site.unregister(Group) # Unregister AdminSite GROUP