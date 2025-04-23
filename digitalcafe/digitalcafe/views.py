from django.shortcuts import render, redirect, get_object_or_404
from .models import item, order_item, order
from .forms import RegisterForm
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required

def openpos(request):
    items = item.objects.filter(stock_quantity__gt=0)
    return render (request, 'digitalcafe/openpos.html', {'items':items})

#    return render (request, 'digitalcafe/openpos.html')

@login_required
def list_item(request):
   allitems = item.objects.all()
   return render(request, 'digitalcafe/list_item.html', {'items':allitems})

@login_required
def to_add(request):
    return render(request, 'digitalcafe/add_item.html')

@login_required
def view_orders(request):
    orders = order.objects.all().order_by('-pk')
    itemorders = order_item.objects.all()
    return render (request, 'digitalcafe/view_orders.html', {'orders':orders, 'items':itemorders})


@login_required
def add_item(request):
   if(request.method == "POST"):
       itname = request.POST.get("item_name")
       itname = itname.capitalize()
       itprice = request.POST.get("item_price")
       stock_quantity = request.POST.get('stock_quantity')
       item.objects.create(item_name=itname, item_price=itprice, stock_quantity=stock_quantity)
       return redirect('list_item')
   else: #return to add_item.html page
       return render (request, 'digitalcafe/add_item.html')


@login_required
def delete_item(request, pk):
   item.objects.filter(pk=pk).delete()
   return redirect('list_item')

@login_required
def edit_item(request, pk):
    
    if (request.method =="POST"):
        item_name = request.POST.get('item_name')
        item_price = request.POST.get('item_price')
        stock_quantity = request.POST.get('stock_quantity')
        item.objects.filter(pk=pk).update(item_name=item_name, item_price=item_price, stock_quantity=stock_quantity)
        return redirect('list_item')
    else:
        i = get_object_or_404(item, pk=pk)
        print(i)
        return render (request, 'digitalcafe/edit_item.html', {'i':i})
    
@login_required
def confirm_order(request):
    if(request.method == "POST"):
        ptype = request.POST.get("payment_method")
        items = request.POST.get("complete_order")
        if not items:
            messages.error(request, "Please select items.")
            return redirect('openpos')
        totamt = request.POST.get("total_amount")
        
        print(items)
        item_fixed = items[:-1]
        stuff = item_fixed.split("-")
        toadd=[]
        for it in stuff:
            itemid, itemq = it.split(':')
            itemq = int(itemq)
            item_obj = item.objects.get(pk=itemid)
            itprice = item_obj.getPrice()
            if itemq>item_obj.getQuantity():
                messages.error(request, item_obj.getName()+" quantity ordered exceeds stock quantity ("+str(item_obj.getQuantity())+")")
                return redirect('openpos')
            lt = itprice * int(itemq)
            toadd.append([item_obj, lt, itemq])
        ord = order.objects.create(total_amount=totamt, payment_type=ptype)
        for x in toadd:
            order_item.objects.create(item_id = x[0], order_id = ord, line_total=x[1], quantity=x[2])
            old_quantity = x[0].getQuantity()
            new_quantity = old_quantity-x[2]
            item.objects.filter(pk=x[0].pk).update(stock_quantity=new_quantity)
   
    messages.success(request, "Order Received")
    return redirect('openpos')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})



class login_view(LoginView):
    template_name = 'digitalcafe/login.html'

class logout_view(LogoutView):
    next_page = 'openpos'