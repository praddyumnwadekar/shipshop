from .models import Category

# we can use this in all the templates 
def menu_links(request):
    links = Category.objects.all()
    return dict(links = links)
