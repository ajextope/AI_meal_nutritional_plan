from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .ai.core_nlp.query_processor import NutritionQueryProcessor
from .ai.recommenders.meal_recommender import MealRecommender
from .models import MealPlan, FoodItem
from .utils import generate_pdf_report
import json
import os

@login_required
def meal_planner_view(request):
    if request.method == 'POST':
        # Process user query
        processor = NutritionQueryProcessor()
        user_input = request.POST.get('dietary_needs', '')
        
        # Detect constraints
        detected_allergies = processor.detect_allergies(user_input)
        
        # Get recommendations
        recommender = MealRecommender(os.path.join('data', 'daily_food_nutrition_dataset.csv'))
        recommendations = recommender.generate_plan({
            'allergies': detected_allergies,
            'budget': request.user.userprofile.budget
        })
        
        # Generate PDF
        pdf_path = generate_pdf_report(recommendations)
        
        # Save meal plan
        MealPlan.objects.create(
            user=request.user,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            daily_plans=recommendations.to_dict(),
            nutritional_summary=recommendations[['Calories (kcal)', 'Protein (g)']].mean().to_dict(),
            shopping_list=self._generate_shopping_list(recommendations),
            pdf=pdf_path
        )
        
        return redirect('plan_detail', plan_id=...)
    
    return render(request, 'planner/form.html')

def _generate_shopping_list(self, recommendations):
    # Implement shopping list logic
    return {'items': list(recommendations['Food_Item'].unique())}

@login_required
def plan_detail_view(request, plan_id):
    plan = get_object_or_404(MealPlan, id=plan_id, user=request.user)
    context = {
        'plan': plan,
        'nutrition': json.loads(plan.nutritional_summary),
        'meals': pd.DataFrame(json.loads(plan.daily_plans))
    }
    return render(request, 'planner/detail.html', context)

@login_required
def profile_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        profile.budget = request.POST.get('budget')
        profile.allergies = json.loads(request.POST.get('allergies'))
        profile.save()
        return redirect('profile')
    return render(request, 'auth/profile.html', {'profile': profile})

@login_required
def image_upload_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # Save image temporarily
        temp_path = os.path.join('media', 'uploads', image.name)
        with open(temp_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Process image
        integrator = CrossModalIntegrator()
        recipe = integrator.image_to_recipe(temp_path)
        
        return render(request, 'planner/image_result.html', {'recipe': recipe})
    
    return render(request, 'planner/image_upload.html')