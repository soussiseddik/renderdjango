from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Q
# Create your views here.

def index(request):
    pattern = ''
    on_search = mssg = False
    prods = []
    all_prods = Product.objects.all()
    if 'Search' in request.GET:
        on_search = True
        pattern = request.GET['Search']
        prods = Product.objects.filter(Q(name__iexact= pattern) | Q(name__contains= pattern))
        if len(prods) == 0:
            mssg = True
    else:
        prods = all_prods
    contex = {'prods': prods, 'on_search': on_search, 'pattern': pattern, 'mssg': mssg}
    return render(request, 'index.html', contex)

def searchPatterns(request):
    prods = []
    if request.method == 'GET':
        pttrn = request.GET['Search'].lower()
        if pttrn in ['', ' '] or len(pttrn) == 1:
            pttrn = '_-_-_-_'
        else:
            prods = Product.objects.filter(name__contains= pttrn)
            patternsnames = [{'p1': prod.name.lower()[:prod.name.lower().index(pttrn)], 
                            'p2': prod.name.lower()[prod.name.lower().index(pttrn) : prod.name.lower().index(pttrn)+len(pttrn)] , 
                            'p3': prod.name.lower()[prod.name.lower().index(pttrn)+len(pttrn):]} for prod in prods]
            for i, prod in enumerate(prods):
                prod.patternsname = patternsnames[i]
    return render(request, 'searchPatterns.html', {'prods': prods})

def prod_info(request, path_name):
    all_prods = Product.objects.all()
    for prod in all_prods:
        if prod.get_path()==path_name:
            rightProd = prod
            caracters = [{'i': i+1, 'c': caracter} for i, caracter in enumerate(str(prod.caract).split('||')) ]
    return render(request, 'prod_info.html', {'prod': rightProd, 'caracters': caracters})

    
def profile(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('signin')
    return render(request, 'profile.html')

def contact(request):
    return render(request, 'contact.html')


def signup(request):
    context = {}
    passvInv = usernameExist = False
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['eml']
        password = request.POST['pass']
        passwordv = request.POST['passv']
        userInfo = {'first_name':first_name, 'last_name':last_name, 'username':username, 'email':email, 'password':password}
        if password == passwordv :
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, 
                                                email=email, 
                                                password=password,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()
                return redirect('signin')
            else:
                usernameExist = True
        else:
            passvInv = True
        context = {'userInfo':userInfo, 'passvInv':passvInv, 'usernameExist': usernameExist}
    return render(request, 'signup.html', context=context)

def signin(request):
    defaultUsername = ''
    passInv = False
    bothInv = False
    if request.method == 'POST':        
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('index')
        else:
            if User.objects.filter(username=username).exists():
                passInv = True
                defaultUsername = username
            else:
                bothInv = True
            
    data = {'passInv': passInv, 'bothInv': bothInv, 'defaultUsername': defaultUsername}
    return render(request, 'signin.html', data)

def category(request, category_name):
    all_prods = Product.objects.all()
    prods = []
    for prod in all_prods:
        if prod.get_category_display() == category_name:
            prods.append(prod)
    return render(request, 'category.html', {'prods': prods, 'category': category_name})