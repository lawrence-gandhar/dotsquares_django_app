from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db import transaction
import json

from . models import *

from itertools import batched
import hashlib
import datetime

# Homepage
# =================================================================================
class Home(View):

    def get(self, request):
        return render(request, "home.html", {})
    
    def post(self, request):
        email = request.POST["email"].strip()
        passwd = request.POST["passwd"].strip()

        if email and passwd:
            user = authenticate(request, email=email, password=passwd)

            if user:
                login(request, user)
                request.session["user_id"] = user.id
                return redirect("category_view")
        return redirect("home")
    
# Logout
# =================================================================================
def logout_view(request):
    logout(request)
    return redirect('home')

# Category and Product Page
# =================================================================================

class CategoryView(LoginRequiredMixin, View):
    def get(self, request, id=1):
        self.category_id = id

        # Check the Category exists or not then get the list of chidrens
        # =================================================================================
        try:
            Categories.objects.get(id=self.category_id)
        except Categories.ObjectNotFound:
            return render(request, "error.html", {}) 

        categories = Categories.objects.filter(parent_id=self.category_id).values('id', 'name')

        # Get 60 Products for the children categories
        # =================================================================================
        
        def dec_to_str(x):
            x["price"] = str(x["price"])
            return x

        category_list = [self.category_id]
        category_list = category_list + [x["id"] for x in categories]

        product_list = Products.objects.filter(category_id__in = category_list).values('id', 'name', 'price', 'stock', 'image')[:60]
        product_list = tuple(batched(list(map(dec_to_str, product_list)), 6))

        cart_list = []
        try:
            get_my_cart = Cart.objects.get(user_id=request.user.id)
            cart_list = ProductCartMapper.objects.filter(cart_id = get_my_cart.id) \
                .select_related('product') \
                .values(
                    'product_id', 'product__name', 'product__image', 'quantity', 'product__price', 'product__stock'
                )
        except:
            pass

        total_amount = 0
        total_items = 0
        present_in_cart = []

        for x in cart_list:
            total_amount += int(x["quantity"]) * x["product__price"]
            total_items += x["quantity"]
            present_in_cart.append(x["product_id"])  

        context = {
            "categories": categories, 
            "products_list": product_list, 
            "cart_list": cart_list, 
            "total_amount": total_amount,
            "total_items": total_items,
            "present_in_cart": present_in_cart,
        }

        return render(request, "category.html", context)
    
@login_required
def set_product_stock(request):
    if request.method == "GET":
        stock_counter = request.GET.get("stock", 0)
        product_id = request.GET.get("item_id", None)
        quantity = request.GET.get("quantity", 0)

        if product_id:
            try:
                product_ins = Products.objects.get(id=int(product_id))
                product_ins.stock = int(stock_counter)
                product_ins.save()
            except:
                return HttpResponse(0)

        get_my_cart = None
        try:
            get_my_cart = Cart.objects.get(user_id = request.user.id)
        except:
            get_my_cart = Cart.objects.create(user_id = request.user.id)
            
        if get_my_cart and int(quantity) > 0:

            try:
                mapper_ins = ProductCartMapper.objects.get(product_id=product_ins.id, cart_id=get_my_cart.id)
                mapper_ins.quantity = int(quantity)
                mapper_ins.save()
            except:
                ProductCartMapper.objects.create(
                    cart = get_my_cart,
                    product = product_ins,
                    quantity = int(quantity)
                )

            return HttpResponse(1)
    return HttpResponse(0)


@login_required
def delete_item_from_cart(request):

    item_id = request.GET.get("item_id", None)

    if item_id:

        item_id = int(item_id)

        try:
            product = Products.objects.get(id = item_id)
        except:
            return HttpResponse(0)
        
        try:
            get_my_cart = Cart.objects.get(user_id=request.user.id)
        except:
            return HttpResponse(0) 
        
        try:
            ins = ProductCartMapper.objects.get(product_id = item_id, cart_id = get_my_cart.id)
            product.stock += ins.quantity
            product.save()
            ins.delete()
        except:
            return HttpResponse(0)
        return HttpResponse(1)
    return HttpResponse(0)


@login_required
def clear_cart(request):
    try:
        Cart.objects.get(user_id = request.user.id).delete()
        return HttpResponse(1)
    except:
        return HttpResponse(0)
    


@login_required
def place_order(request):
    try:
        with transaction.atomic():

            try:
                cart_ins = Cart.objects.get(user_id = request.user.id)
            except:
                messages.error(request, "No items in the Cart. Please add items and try again.")
                return redirect("category_view")
            
            product_maps = ProductCartMapper.objects.select_related('product').filter(cart_id = cart_ins.id).values(
                'product_id', 'product__name', 'quantity', 'product__price'
            )

            product_json = {
                row["product_id"]: {
                    "product_name": row["product__name"], 
                    "quantity": row["quantity"],
                    "price_per_unit": str(row["product__price"]),
                    "amount": str(row["product__price"] *  row["quantity"])
                } for row in product_maps
            }

            total_amount = str(format(sum([float(product_json[x]["amount"]) for x in product_json.keys()]), ".2f"))
            
            d_time = datetime.datetime.now()

            order_ins = OrderDetails.objects.create(
                user_id = request.user.id,
                total_amount = total_amount,
                products = product_json
            )

            hashed_data = hashlib.sha256((str(order_ins.id)+"_"+d_time.strftime("%Y-%m-%d %H:%M:%S")).encode('utf8')).hexdigest()
            order_ins.order_hash = hashed_data
            order_ins.order_date = d_time
            order_ins.save()
            cart_ins.delete()

            print(product_json, total_amount)
            messages.success(request, "Order placed successfully")
    except:
        messages.error(request, "Unable to place the order. Please try again later")
    return redirect("category_view")