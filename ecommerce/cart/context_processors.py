from cart.models import Cart

def cart_items(request):
     u=request.user
     count=0
     try:
         c=Cart.objects.filter(user=u)

         for i in c:
             count+=i.quantity
     except:
         pass

     return {'count':count}

