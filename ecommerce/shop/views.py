from django.shortcuts import render,redirect
from django.views import View
from shop.models import Category
from shop.forms import SignupForm,LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        context={'category':c}
        return render(request,'categories.html',context)

class ProductView(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'category':c}
        return  render(request,'product.html',context)

from shop.models import Product
class ProductDetail(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,'productdetail.html',context)


class Register(View):
        def get(self, request):
            form_instance =SignupForm()
            return render(request, 'register.html', {'form': form_instance})

        def post(self, request):
            form_instance = SignupForm(request.POST)
            if form_instance.is_valid():
                form_instance.save()
                return redirect('shop:categories')


from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

class Userlogin(View):
    def get(self,requesst):
        form_instance=LoginForm()
        return render(requesst,'login.html',{'form':form_instance})

    def post(self,request):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            name=form_instance.cleaned_data['username']
            pwd=form_instance.cleaned_data['password']
            user=authenticate(username=name,password=pwd) #returns user objects if entered username and password
            #else retrun none

            if user :#if user exists
                login(request,user) #starts a new session with the current user
                return redirect('shop:categories')
            else:
                # print('invalid credentials')
                messages.error=(request,'Inavlid Credentails, Please enter valid username and password')
                return render(request,'login.html',{'form':form_instance})

class Userlogout(View):
    def get(self,request):
        logout(request)
        return redirect('shop:categories')

from shop.forms import CategoryForm

class AddCategory(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self,request):
        form_instance=CategoryForm()
        return render(request,'addcategory.html',{'form':form_instance})


    def post(self,request):
        form_instance=CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')

from shop.forms import ProductForm

class AddProduct(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_fuc(self):
        return self.request.user.is_superuser

    def get(self,request):
        form_instance=ProductForm()
        return render(request, 'addproduct.html', {'form': form_instance})


    def post(self,request):
        form_instance=ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')

from shop.forms import StockForm

class AddStock(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=StockForm(instance=p)
        return render(request,'addstock.html',{'form':form_instance})

    def post(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=StockForm(request.POST,instance=p)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')


from django.db.models import Q

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        products = []
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(category__name__icontains=query)
            ).distinct()

        context = {'products': products, 'query': query}
        return render(request, 'search.html', context)





