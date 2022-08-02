
from django.shortcuts import render,get_object_or_404

from category.models import Category
from .models import Product
from orders.models import orderproduct

# Create your views here.

def store(request,category_slug=None):
   categories= None
   products=None
   
   if category_slug !=None:
      categories=get_object_or_404(Category,slug=category_slug)
      products=Product.objects.filter(category=categories,is_available=True)
      product_count=products.count()
   else:
      products = Product.objects.all().filter(is_available=True)
      product_count = products.count()
   
   context = {
      'products': products,
      'product_count': product_count,
   }
   return render(request,'store/store.html', context)

def product_detail(request, category_slug ,product_slug):
   try:
      single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
   except Exception as e:
      raise e

   try:
      orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
   except OrderProduct.DoesNotExist:
      orderproduct = None

   
   #get the reviews
   reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

       
   context={
          'single_product':single_product,
          'reviews': reviews,
       }
   return render(request,'store/product_detail.html',context)