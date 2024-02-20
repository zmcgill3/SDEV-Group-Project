from django.urls import path
from . import views

urlpatterns = [
    path("", views.displayInitialTemplate),
    path("recipefornow", views.getDataForNow, name='getDataForNow'),
    path("recipeforlater", views.getDataForLater, name = 'getDataForLater'),
    path('submit/', views.submitIngredients, name='submitIngredients'),
    path('submitforlater/', views.submitIngredientsForLater, name='submitIngredientsForLater')
    ]