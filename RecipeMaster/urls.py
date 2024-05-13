from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.displayInitialTemplate, name='home'),
    path("home", views.displayInitialTemplate, name='home'),
    path("recipefornow", views.getDataForNow, name='getDataForNow'),
    path("recipeforlater", views.getDataForLater, name = 'getDataForLater'),
    path('submit/', views.submitIngredients, name='submitIngredients'),
    path('submitforlater/', views.submitIngredientsForLater, name='submitIngredientsForLater'),
    path('clear/', views.clearIngredients, name='clearIngredients'),
    path('clearForLater/', views.clearIngredientsForLater, name='clearIngredientsForLater'), #Since I am referencing the name directly in the html template it is okay that this path and the one above have the same route or url ending of clear
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('passwordreset/', views.passwordReset, name='passwordReset'),
    path('signup/', views.signUp, name='signUp'),
    path('grocery-list', views.showGroceryList, name='grocery-list'),
    path('savedRecipes', views.showSavedRecipes, name='savedRecipes'),
    path('pantry', views.showPantry, name='pantry'),
    path('importForLater', views.importForLater, name='importForLater'),
    path('importForNow', views.importForNow, name='importForNow'),
    path('saveRecipe', views.saveRecipe, name='saveRecipe'),
    path('saveRecipeForNow', views.saveRecipeForNow, name='saveRecipeForNow'),
    path('clearSavedRecipes', views.clearSavedRecipes, name='clearSavedRecipes'),
    path('groceryResults', views.groceryResults, name='groceryResults')
    ]