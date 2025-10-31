from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, UserReputation


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'phone', 'role', 'is_verified', 'reputation_score', 'is_active', 'date_joined']
    list_filter = ['role', 'is_verified', 'is_active', 'date_joined']
    search_fields = ['email', 'phone', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Additional Info'), {
            'fields': ('phone', 'role', 'is_verified', 'phone_verified', 'email_verified', 
                      'mfa_enabled', 'reputation_score', 'blockchain_wallet_address')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'organization', 'language']
    search_fields = ['user__email', 'department', 'organization', 'badge_number']


@admin.register(UserReputation)
class UserReputationAdmin(admin.ModelAdmin):
    list_display = ['user', 'accuracy_score', 'report_count', 'verified_reports', 'false_reports', 'spam_count']
    list_filter = ['last_reputation_update']
    search_fields = ['user__email']

