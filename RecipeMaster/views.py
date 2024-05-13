from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from forms import SignUpForm
from django.conf import settings
from django.contrib.auth import login, authenticate
import os
# Create your views here.

def loadUniqueIngredients():
    # Construct the full file path
    file_path = os.path.join(settings.STATIC_ROOT, 'uniqueIngredients.txt')

    # Open the file and read lines
    with open(file_path, 'r') as file:
        ingredientNames = file.read().splitlines()

    return ingredientNames

def loadInOrderIngredients():
    file_path = os.path.join(settings.STATIC_ROOT, 'mostRecentNERLimitRows1.txt')
    file_path2 = os.path.join(settings.STATIC_ROOT, 'mostRecentNERLimitRows2.txt')

    ingredients_in_order = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()[4:-4]
            line = line.split('"", ""')
            ingredients_in_order.append(line)

    with open(file_path2, 'r') as file:
        for line in file:
            line = line.strip()[4:-4]
            line = line.split('"", ""')
            ingredients_in_order.append(line)

    return ingredients_in_order

def loadRecipeNames():
    file_path = os.path.join(settings.STATIC_ROOT, 'dishNames.txt')
    file = open(file_path, "r")
    recipeNamesInOrder = []
    for line in file:
        recipeNamesInOrder.append(line)
    file.close()
    return recipeNamesInOrder

def isContained(recipeIngredients,userIngredients):
    if(all(x in userIngredients for x in recipeIngredients)):
        return True
    else:
        return False

def loadLinks():
    file_path = os.path.join(settings.STATIC_ROOT, 'links.txt')
    file = open(file_path, "r")
    links = []
    for line in file:
        links.append(line)
    file.close()
    return links

def loadAmounts():
    file_path = os.path.join(settings.STATIC_ROOT, 'amountsAndIngredients1.txt')
    file_path2 = os.path.join(settings.STATIC_ROOT, 'amountsAndIngredients2.txt')
    file_path3 = os.path.join(settings.STATIC_ROOT, 'amountsAndIngredients3.txt')

    file = open(file_path, "r")
    amountsList = []
    for line in file:
       line = line.strip()[4:-4]
       line = line.split('"", ""')
       amountsList.append(line)

    file = open(file_path2, "r")
    for line in file:
       line = line.strip()[4:-4]
       line = line.split('"", ""')
       amountsList.append(line)

    file = open(file_path3, "r")
    for line in file:
       line = line.strip()[4:-4]
       line = line.split('"", ""')
       amountsList.append(line)

    return amountsList


@login_required #Denys access to views and templates unless logged in
def displayInitialTemplate(request):
    return render(request, "initial.html")

@login_required #Denys access to views and templates unless logged in
def getDataForLater(request):
    query = request.GET.get('ingredient', '')
    uniqueIngredientNames = loadUniqueIngredients()
    error_message = None
    error_message = request.session.get('error_message', None)
    if request.method == 'POST':
        ingredient = request.POST.get('ingredient')
        if ingredient:
            ingredients = request.session.get('ingredientsForLater', [])
            if ingredient in ingredients:
                error_message = "Ingredient has already been entered"
            else:
                ingredients.append(ingredient)
                request.session['ingredientsForLater'] = ingredients
                return redirect('getDataForLater')
    ingredients = request.session.get('ingredientsForLater', [])
    request.session.pop('error_message', None)  # Removes any previous error message
    return render(request, 'recipeForLater.html', {'query': query, 'uniqueIngredientNames': uniqueIngredientNames, 'ingredients': ingredients, 'error': error_message})

@login_required #Denys access to views and templates unless logged in
def getDataForNow(request):
    query = request.GET.get('ingredient', '')
    uniqueIngredientNames = loadUniqueIngredients()
    error_message = None
    error_message = request.session.get('error_message', None)
    if request.method == 'POST':
        ingredient = request.POST.get('ingredient')
        if ingredient:
            ingredients = request.session.get('ingredients', [])
            if ingredient in ingredients:
                error_message = "Ingredient has already been entered"
            else:
                ingredients.append(ingredient)
                request.session['ingredients'] = ingredients
                return redirect('getDataForNow')
    ingredients = request.session.get('ingredients', [])
    request.session.pop('error_message', None)  # Removes any previous error message
    return render(request, 'recipeForNow.html', {'query': query, 'uniqueIngredientNames': uniqueIngredientNames, 'ingredients': ingredients, 'error': error_message})

@login_required #Denys access to views and templates unless logged in
def submitIngredients(request):
	ingredients = request.session.get('ingredients', [])
	recipeIngredients = loadInOrderIngredients()
	found = []
	recipes =[]
	message = ""
	count = 0
	for list in recipeIngredients:
		if(len(found) >= 10):
			break
		elif(len(ingredients) < len(list)):
			count += 1
			continue
		elif(isContained(list, ingredients)):
			found.append(count)
			count += 1
			continue
		else:
			count += 1
	recipeNames = loadRecipeNames()
	links = loadLinks()
	amountsOfIngredients = loadAmounts()
	for x in range(len(found)):
		recipe = {
			'name': recipeNames[found[x]],
			'ingredients': recipeIngredients[found[x]],
			'amounts': amountsOfIngredients[found[x]],
			'link': links[found[x]]
		}
		recipes.append(recipe)
	if(len(found) == 0):
		message += "We weren't able to find any recipes that incorporate all the ingredients you listed."
		message += "We recommend removing some ingredients and ensuring you use the auto suggested ingredients to match our records and avoid typos!"
	else:
		message = None

	request.session['recipes'] = recipes
	request.session['message'] = message
	return render(request, 'resultsForNow.html', {'recipes': recipes, 'message': message})

@login_required #Denys access to views and templates unless logged in
def submitIngredientsForLater(request):
	ingredients = request.session.get('ingredientsForLater', [])
	recipeIngredients = loadInOrderIngredients()
	found = []
	recipes =[]
	message = ""
	count = 0
	for list in recipeIngredients:
		if(len(found) >= 10):
			break
		elif(len(ingredients) >= len(list)):    #This is just the opposite of recipe for later because we want recipes that contain our users list instead of the other way around
			count += 1
			continue
		elif(isContained(ingredients, list)):   #This is just the opposite of recipe for later because we want recipes that contain our users list instead of the other way around
			found.append(count)
			count += 1
			continue
		else:
			count += 1

	recipeNames = loadRecipeNames()
	links = loadLinks()
	amountsOfIngredients = loadAmounts()
	for x in range(len(found)):
		recipe = {
			'name': recipeNames[found[x]],
			'ingredients': recipeIngredients[found[x]],
			'amounts': amountsOfIngredients[found[x]],
			'link': links[found[x]]
		}
		recipes.append(recipe)
	if(len(found) == 0):
		message += "We weren't able to find any recipes that incorporate all the ingredients you listed."
		message += "We recommend removing some ingredients and ensuring you use the auto suggested ingredients to match our records and avoid typos!"
	else:
		message = None
	request.session['ingredientsForLater'] = []
	request.session['recipes'] = recipes
	request.session['message'] = message
	return render(request, 'resultsForLater.html', {'recipes': recipes, 'message': message})

def clearIngredients(request):
    if 'ingredients' in request.session:
        del request.session['ingredients']
    return redirect('getDataForNow')

def clearIngredientsForLater(request):
    if 'ingredientsForLater' in request.session:
        del request.session['ingredientsForLater']
    return redirect('getDataForLater')

#def passwordReset(request):
#    return redirect('login')

def signUp(request):
    if(request.method == "POST"):
        form = SignUpForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required #Denys access to views and templates unless logged in
def showGroceryList(request):
    query = request.GET.get('ingredient', '')
    uniqueIngredientNames = loadUniqueIngredients()
    if request.method == 'POST':
        ingredient = request.POST.get('ingredient')
        if ingredient:
            ingredients = request.session.get('groceryIngredients', [])
            ingredients.append(ingredient)
            request.session['groceryIngredients'] = ingredients
            return redirect('grocery-list')
    ingredients = request.session.get('groceryIngredients', [])

    return render(request, "grocery-list.html", {'query': query, 'uniqueIngredientNames': uniqueIngredientNames, 'ingredients': ingredients})

@login_required #Denys access to views and templates unless logged in
def showSavedRecipes(request):
    savedRecipes = request.session.get('savedRecipes', [])
    return render(request, "savedRecipes.html", {'recipes': savedRecipes})

@login_required #Denys access to views and templates unless logged in
def showPantry(request):
    query = request.GET.get('ingredient', '')
    uniqueIngredientNames = loadUniqueIngredients()
    if request.method == 'POST':
        ingredient = request.POST.get('ingredient')
        if ingredient:
            ingredients = request.session.get('pantryIngredients', [])
            ingredients.append(ingredient)
            request.session['pantryIngredients'] = ingredients
            return redirect('pantry')
    ingredients = request.session.get('pantryIngredients', [])
    return render(request, "pantry.html", {'query': query, 'uniqueIngredientNames': uniqueIngredientNames, 'ingredients': ingredients})

def importForLater(request):
    duplicates_found = False
    pantryIngredients = request.session.get('pantryIngredients', [])
    ingredients = request.session.get('ingredientsForLater', [])
    for item in pantryIngredients:
        if item not in ingredients:
            ingredients.append(item)
        else:
            duplicates_found = True
    request.session['ingredientsForLater'] = ingredients

    if duplicates_found:
        request.session['error_message'] = "One or more items weren't imported because they were duplicates."
    else:
        request.session.pop('error_message', None)  # Removes any previous error message

    return redirect('getDataForLater')

def importForNow(request):
    duplicates_found = False
    pantryIngredients = request.session.get('pantryIngredients', [])
    ingredients = request.session.get('ingredients', [])
    for item in pantryIngredients:
        if item not in ingredients:
            ingredients.append(item)
        else:
            duplicates_found = True
    request.session['ingredients'] = ingredients

    if duplicates_found:
        request.session['error_message'] = "One or more items weren't imported because they were duplicates."
    else:
        request.session.pop('error_message', None)  # Removes any previous error message

    return redirect('getDataForNow')

@login_required #Denys access to views and templates unless logged in
def saveRecipe(request):
    name = request.POST.get('recipe_name')
    ingredients = request.POST.get('recipe_ingredients').split(', ')
    link = request.POST.get('recipe_link')
    amounts = request.POST.get('recipe_amounts').split(', ')
    recipe = {
    'name': name,
    'ingredients': ingredients,
    'amounts': amounts,
    'link': link
    }
    savedRecipes = request.session.get('savedRecipes', [])
    savedRecipes.append(recipe)
    request.session['savedRecipes'] = savedRecipes
    message= request.session.get('message')
    recipes = request.session.get('recipes', [])
    return render(request, 'resultsForLater.html', {'recipes': recipes, 'message': message})

@login_required #Denys access to views and templates unless logged in
def saveRecipeForNow(request):
    name = request.POST.get('recipe_name')
    ingredients = request.POST.get('recipe_ingredients').split(', ')
    link = request.POST.get('recipe_link')
    amounts = request.POST.get('recipe_amounts').split(', ')
    recipe = {
    'name': name,
    'ingredients': ingredients,
    'amounts': amounts,
    'link': link
    }
    savedRecipes = request.session.get('savedRecipes', [])
    savedRecipes.append(recipe)
    request.session['savedRecipes'] = savedRecipes
    message= request.session.get('message')
    recipes = request.session.get('recipes', [])
    return render(request, 'resultsForNow.html', {'recipes': recipes, 'message': message})

def clearSavedRecipes(request):
    if 'savedRecipes' in request.session:
        del request.session['savedRecipes']
    return redirect('savedRecipes')

@login_required #Denys access to views and templates unless logged in
def groceryResults(request):
    query = request.GET.get('ingredient', '')
    uniqueIngredientNames = loadUniqueIngredients()
    if request.method == 'POST':
        ingredients = request.session.get('groceryIngredients', [])
        meals = generate_meals(ingredients)
        request.session['meals'] = meals
        return render(request, "grocery-list.html", {'query': query, 'uniqueIngredientNames': uniqueIngredientNames, 'ingredients': ingredients, 'meals':meals})

    ingredients = request.session.get('groceryIngredients', [])
    return render(request, "grocery-list.html", {'query': query, 'uniqueIngredientNames': uniqueIngredientNames, 'ingredients': ingredients})

def generate_meals(ingredients):
	recipeIngredients = loadInOrderIngredients()
	found = []
	recipes =[]
	count = 0
	for list in recipeIngredients:
		if(len(found) >= 10):
			break
		elif(len(ingredients) < len(list)):
			count += 1
			continue
		elif(isContained(list, ingredients)):
			found.append(count)
			count += 1
			continue
		else:
			count += 1
	recipeNames = loadRecipeNames()
	links = loadLinks()
	amountsOfIngredients = loadAmounts()
	for x in range(len(found)):
		recipe = {
			'name': recipeNames[found[x]],
			'ingredients': recipeIngredients[found[x]],
			'amounts': amountsOfIngredients[found[x]],
			'link': links[found[x]]
		}
		recipes.append(recipe)
	if(len(found) == 0):
		recipes = []
	return recipes
