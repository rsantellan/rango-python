from django.shortcuts import render

from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm

def index(request):

    context_dict = {}
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-like')[:5]

    pages_list = Page.objects.order_by('-views')[:5]
    context_dict['categories'] = category_list
    context_dict['pages'] = pages_list

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'rango/index.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}
    try:
        # Trying to get the category of the slug.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        context_dict['category'] = category
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

    except Category.DoesNotExist:
        # It'll be empty
        pass
    return render(request, 'rango/category.html', context_dict)



def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def about(request):
    return HttpResponse("This is an about page. <br/> <a href='/rango/'>Index</a>")