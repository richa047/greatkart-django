from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)# pass in navbar.html line 42