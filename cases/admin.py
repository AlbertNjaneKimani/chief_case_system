from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, Case, Appointment

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profiles'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Register the customized User admin and other models
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Case)
admin.site.register(Appointment)