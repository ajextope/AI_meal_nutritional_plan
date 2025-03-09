from django.contrib import admin
from .models import FoodItem, UserProfile, MealPlan

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'calories', 'price')
    search_fields = ('name', 'category')
    list_filter = ('category', 'meal_type')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'budget', 'health_goals')
    search_fields = ('user__username', 'health_goals')

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date')
    date_hierarchy = 'start_date'