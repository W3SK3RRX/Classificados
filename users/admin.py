from django.contrib import admin
from .models import Plan, Subscription, User

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration_in_days')
    search_fields = ('name',)
    list_filter = ('price',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'start_date', 'end_date', 'active')
    search_fields = ('user__email',)
    list_filter = ('active', 'end_date')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'lastname', 'user_type', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'lastname')
    list_filter = ('user_type', 'is_active', 'is_staff')
