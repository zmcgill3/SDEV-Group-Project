from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
# Create your views here.

def loadUniqueIngredients():
    with open('/mnt/c/Users/zackm/Desktop/mysite/RecipeMaster/uniqueIngredients.txt', 'r') as file:
        ingredientNames = file.read().splitlines()
    return ingredientNames

def loadInOrderIngredients():
    file = open("/mnt/c/Users/zackm/Desktop/mysite/RecipeMaster/ingredients.txt", "r")
    ingredientsInOrder = []
    for line in file:
        items = line.strip()[1:-1].split(", ")
        ingredientsInOrder.append(items)
    file.close()
    return ingredientsInOrder

def loadRecipeNames():
    file = open("/mnt/c/Users/zackm/Desktop/mysite/RecipeMaster/dishNames.txt", "r")
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
    file = open("/mnt/c/Users/zackm/Desktop/mysite/RecipeMaster/links.txt", "r")
    links = []
    for line in file:
        links.append(line)
    file.close()
    return links

def loadAmounts():
    file = open("/mnt/c/Users/zackm/Desktop/mysite/RecipeMaster/amountsAndIngredients.txt", "r")
    amountsList = []
    for line in file:
       line = line.strip()[4:-4]
       line = line.split('"", ""')
       amountsList.append(line)
    return amountsList



def displayInitialTemplate(request):
    return render(request, "initial.html")

def getDataForLater(request):
    query = request.GET.get('ingredient', '')
    uniqueIngredientNames = loadUniqueIngredients()
    if request.method == 'POST':
        ingredient = request.POST.get('ingredient')
        if ingredient:
            ingredients = request.session.get('ingredients', [])
            ingredients.append(ingredient)
            request.session['ingredients'] = ingredients
            return redirect('getDataForLater')
    ingredients = request.session.get('ingredients', [])
    return render(request, 'recipeForLater.html', {'query': query, 'uniqueIngredientNames': uniqueIngredientNames, 'ingredients': ingredients})


def getDataForNow(request):
    query = request.GET.get('ingredient', '')
    uniqueIngredientNames = loadUniqueIngredients()
    if request.method == 'POST':
        ingredient = request.POST.get('ingredient')
        if ingredient:
            ingredients = request.session.get('ingredients', [])
            ingredients.append(ingredient)
            request.session['ingredients'] = ingredients
            return redirect('getDataForNow')
    ingredients = request.session.get('ingredients', [])
    
    return render(request, 'recipeForNow.html', {'query': query, 'uniqueIngredientNames': uniqueIngredientNames, 'ingredients': ingredients})

def submitIngredients(request):
    ingredients = request.session.get('ingredients', [])
    recipeIngredients = loadInOrderIngredients()
    found = []
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
    result = ""
    for x in range(len(found)):
        result += "Recipe name: " + recipeNames[found[x]] + "<br>"
        result += "Ingredients: " + ", ".join(recipeIngredients[found[x]]) + "<br>"
        result += "Amounts:" + "<br>"
        for elem in amountsOfIngredients[found[x]]:
            result += "&nbsp;"*17 + elem + "<br>"
        result += "Link: " + links[found[x]] + "<br>"
        result += "<br>"
    if(len(found) == 0):
        result += "We weren't able to find any recipes that can be made with only what you have on hand." + "<br>"
        result += "We recommend adding more ingredients if you have more on hand or check out our recipes for later mode!"
    
    request.session['ingredients'] = []
    result = mark_safe(result)
    return render(request, 'resultsForNow.html', {'result':result})

def submitIngredientsForLater(request):
    ingredients = request.session.get('ingredients', [])
    recipeIngredients = loadInOrderIngredients()
    found = []
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
    result = ""
    links = loadLinks()
    amountsOfIngredients = loadAmounts()
    for x in range(len(found)):
        result += "Recipe name: " + recipeNames[found[x]] + "<br>"
        result += "Ingredients: " + ", ".join(recipeIngredients[found[x]]) + "<br>"
        result += "Amounts:" + "<br>"
        for elem in amountsOfIngredients[found[x]]:
            result += "&nbsp;"*17 + elem + "<br>"
        result += "Link: " + links[found[x]] + "<br>"
        result += "<br>"
    if(len(found) == 0):
        result += "We weren't able to find any recipes that incorporate all the ingredients you listed." + "<br>"
        result += "We recommend removing some ingredients and ensuring you use the auto suggested ingredients to match our records and avoid typos!"
    
    request.session['ingredients'] = []
    result = mark_safe(result)
    return render(request, 'resultsForLater.html', {'result':result})