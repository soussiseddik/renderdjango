from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
AllProducts = Product.objects.all()

def index(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    pattern = ''
    on_search = mssg = False
    prods = []
    all_prods = AllProducts
    if 'Search' in request.GET:
        on_search = True
        pattern = request.GET['Search'].lower()
        prods = Product.objects.filter(name__contains= pattern) | Product.objects.filter(category__contains= pattern)
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
        if not(pttrn in ['', ' '] or len(pttrn) == 1):
            prods = Product.objects.filter(name__contains= pttrn)
            print(len(prods)==0)
            patternsnames = [{'p1': prod.name.lower()[:prod.name.lower().index(pttrn)], 
                            'p2': prod.name.lower()[prod.name.lower().index(pttrn) : prod.name.lower().index(pttrn)+len(pttrn)] , 
                            'p3': prod.name.lower()[prod.name.lower().index(pttrn)+len(pttrn):]} for prod in prods]
            for i, prod in enumerate(prods):
                prod.patternsname = patternsnames[i]
    return render(request, 'searchPatterns.html', {'prods': prods})

def prod_info(request, path_name):
    if not request.user.is_authenticated:
        return redirect('signin')
    all_prods = AllProducts
    for prod in all_prods:
        if prod.get_path()==path_name:
            rightProd = prod
            caracters = [{'i': i+1, 'c': caracter} for i, caracter in enumerate(str(prod.caract).split('||')) ]
    return render(request, 'prod_info.html', {'prod': rightProd, 'caracters': caracters})

    
def profile(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    elif request.method == 'POST':
        auth.logout(request)
        return redirect('signin')
    else:
        return render(request, 'profile.html')

def contact(request):
    if not request.user.is_authenticated:
        return redirect('signin')
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
    if not request.user.is_authenticated:
        return redirect('signin')
    all_prods = AllProducts
    prods = []
    for prod in all_prods:
        if prod.get_category_display() == category_name:
            prods.append(prod)
    return render(request, 'category.html', {'prods': prods, 'category': category_name})