from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from cart.models import Cart,Order_items,Order
from shop.models import Product
from cart.forms import  OrderForm

import razorpay

class AddtoCart(View):
    def get(self,request,i):
        p=Product.objects.get(id=i) #product object
        u=request.user
        try:
            c = Cart.objects.get(user=u,product=p)#if cart object for particular product exists
            c.quantity += 1 #increament by 1
            c.save()

        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()

        return redirect('cart:cartview')

class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.quantity*i.product.price # to find the subtotal

        context={'cart':c,'total': total}
        return render(request,'cart.html',context)



class RemovefromCart(View):
    def get(self, request, i):
        p = Product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=p)
            if c.quantity > 1:
                c.quantity -= 1
                c.save()
            else:
                c.delete()

        except:
            pass

        return redirect('cart:cartview')


class DeletefromCart(View):
    def get(self, request, i):
        p = Product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=p)
            c.delete()

        except:
            pass
        return redirect('cart:cartview')




def check_stock(c):
    stock = True
    for i in c:
        if i.product.stock<i.quantity:
            stock = False
            break
    return stock

from django.contrib import messages
class Checkout(View):
    def get(self,request):
        form_instance = OrderForm()
        return render(request, 'checkout.html', {'form': form_instance})

    def post(self,request):
        print(request.POST)
        u=request.user
        c=Cart.objects.filter(user=u)# all objects selected by the user
        stock=check_stock(c)
        if stock:

            form_instance = OrderForm(request.POST)
            if form_instance.is_valid():
                o = form_instance.save(commit=False)
                o.user = u
                o.save()

                # Total amount
                total = 0
                for i in c:
                    total+=i.quantity*i.product.price

                for i in c:#In each iteration each cart product is added to order_items table
                    order=Order_items.objects.create(order=o,product=i.product,quantity=i.quantity)
                    order.save
                    

                if o.payment_method=="Online":
                    #razorpay connection
                    client=razorpay.Client(auth=('rzp_test_RJOUHvQsrVcuME','BPBC5674zwMmk5xbtxf4G0mz'))
                    #Place order
                    response_payment=client.order.create(dict(amount=total*100,currency='INR'))
                    print(response_payment)
                    order_id=response_payment['id']
                    o.order_id=order_id
                    o.amount=total
                    o.save()

                    context={'payment':response_payment}
                    return render(request,'payment.html',context)

                elif o.payment_method=="COD":
                    o.is_ordered=True
                    o.amount=total
                    o.save()

                    items=Order_items.objects.filter(order=o)
                    for i in items:
                        i.product.stock-=i.quantity
                        i.product.save()
                        print(i.product.stock)

                    c.delete()
                    return render(request, 'paymentsuccess.html')

                else:
                    pass

        else:
            messages.error(request,'Currently Items not available, please try again later')

            return render(request,'payment.html')

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import  login

@method_decorator(csrf_exempt,name="dispatch")
class PaymentSuccess(View):

    def post(self, request,i):
        u=User.objects.get(username=i)
        login(request,u)
        response=request.POST #order_id,signature,razorpay payment_id
        print(response)
        id=response['razorpay_order_id']
        o=Order.objects.get(order_id=id)
        o.is_ordered=True
        o.save()

        #to reduce stock
        items=Order_items.objects.filter(order=o)
        print(items)
        for i in items:
            i.product.stock-=i.quantity
            i.product.save()

        # Cart.objects.filter(user=o.user).delete()
        c=Cart.objects.filter(user=u)
        c.delete()

        return render(request, 'paymentsuccess.html')


class OrderSummary(View):
    def get(self, request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'orders':o}
        return render(request,'ordersummary.html',context)

