from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.views import View
from .models import Product, Review, Category, Cart, CartItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.


# class ProductListView(View):
#     def get(self, request):
#         product = Products.objects.all().order_by('-create_at')
#         return render(request, 'product/product_list.html', {'product': product})


class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ProductCreateView(CreateView):
    model = Product
    template_name = 'product/product_create.html'
    fields = '__all__'
    success_url = reverse_lazy('products:product-list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('products:product-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        reviews = Review.objects.filter(product=pk)
        related_products = Product.objects.filter(category=product.category).exclude(id=pk)[:5]
        context = {
            'product': product,
            'reviews': reviews,
            'related_products': related_products,
        }
        return render(request, 'product/product_detail.html', context=context)

    def post(self, request, pk):
        product = Product.objects.get(id=pk)
        if request.method == 'POST':
            if 'delete_review' in request.POST:
                review_id = request.POST.get('delete_review')
                review = Review.objects.get(id=review_id)
                review.delete()
            else:
                comment = request.POST.get('comment')
                star_given = int(request.POST.get('star_given'))
                if request.user.is_authenticated:
                    user = request.user
                else:
                    user = None  # Assign None for anonymous user
                review = Review.objects.create(
                    comment=comment,
                    star_given=star_given,
                    product=product,
                    user=user
                )
                review.save()
        return redirect('products:product-detail', pk=pk)


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart-detail')


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'products/cart_detail.html'
    context_object_name = 'cart'

    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)


class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, pk):
        cart_item = get_object_or_404(CartItem, id=pk)
        cart_item.delete()
        return redirect('cart-detail')


