emailid,pswd
rpricha4@gmail.com,Linux@123.
1.django-admin startproject greatkart 
2.create views home.
3.write urls for the same
4.create templates folder in Greatkart project(outter folder ie root folder)
5.note- if u do not have aap and create templates folder in Outter project 
folder then name it in settings.py file dir['templates']
6.copy index.html in home.html
7.configure static filess
note -greatkart(inner proj folder)/static
8.now download genkart template folder (for readymade template)
9.now copy font,css,images,js folder to static folder in your project.
10.STATIC_ROOT = BASE_DIR '/static' # basic_dir is greatkart(inner folder)
STATICFILES_DIRS = [ 'greatkart/static',]
11.collect static command and will create new static folder under root project folder
  ie static folder created under root project folder(outter proj folder)
   "python3 manage.py collectstatic".note it also called folder admin
12. load staic inside home.shtml file and make all static links as s=dynamic by adding {% static 'images/items/3.jpg' %}
13.now create base.html and shuffle basic  common code in it from home.html
14.create includes for common things like footer,navbar.

_________________________________________________create app(category,order,store,product)______________________________________
1.create app category- python3 manage.py startapp category.
2.declare category app in settings.py
3.register Category model in admin.py,python3 manage.py makemigrations,python3 manage.py migrate,create superuser.
4.instal pillow .
*custom user model(so that u can login using email n pswd in sdmin panel)
1.create accounts app.declare it in settings
2.create custom module accounts(model,admin)
----------------------configuring media files-------------------------------------------
1.MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR /'media'
 *) 
 glenkart(urls.py) add
+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
2.download category images,and upload category data from admin panel.
folder4 video6-
3.fixing slug autopuplate from category field using admin.py,
4.add data for category model from admin panel.
------------------store app
f5v1
1.python3 manage.py startapp store
--------------f6v3-------------------
1.

