from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    calories = models.FloatField(validators=[MinValueValidator(0)])
    protein = models.FloatField(validators=[MinValueValidator(0)])
    carbohydrates = models.FloatField(validators=[MinValueValidator(0)])
    fat = models.FloatField(validators=[MinValueValidator(0)])
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    allergens = models.CharField(max_length=255, blank=True)
    meal_type = models.CharField(max_length=50, choices=[
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack')
    ])

    def __str__(self):
        return f"{self.name} ({self.category})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dietary_preferences = models.JSONField(default=dict)
    allergies = models.JSONField(default=list)
    budget = models.FloatField(default=0.0, validators=[MinValueValidator(0)])
    health_goals = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    daily_plans = models.JSONField()  # Stores structured meal data
    nutritional_summary = models.JSONField()
    shopping_list = models.JSONField()
    pdf = models.FileField(upload_to='meal_plans/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Meal Plan {self.start_date} to {self.end_date}"