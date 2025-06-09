from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PlayerProfile, RefereeProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'location', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'location', 'profile_photo')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(PlayerProfile)
admin.site.register(RefereeProfile)
