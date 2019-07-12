from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pet_logic import views


router = DefaultRouter()
router.register('', views.PetsViewSet)
# router.register('ingredients', views.IngredientViewSet)
# router.register('recipes', views.RecipeViewSet)

app_name = 'pet_logic'

urlpatterns = [
    path('', include(router.urls))
]
