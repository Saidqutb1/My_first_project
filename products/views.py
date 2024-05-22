from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.views import View
from .models import Products, Review, Category
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


# class ProductListView(View):
#     def get(self, request):
#         product = Products.objects.all().order_by('-create_at')
#         return render(request, 'product/product_list.html', {'product': product})


class ProductListView(ListView):
    model = Products
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
    model = Products
    template_name = 'product/product_create.html'
    fields = '__all__'
    success_url = reverse_lazy('products:product-list')


class ProductDeleteView(DeleteView):
    model = Products
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('products:product-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context


class ProductDetailView(View):
    def get(self, request, pk):
        product = Products.objects.get(id=pk)
        reviews = Review.objects.filter(product=pk)
        related_products = Products.objects.filter(category=product.category).exclude(id=pk)[:5]
        context = {
            'product': product,
            'reviews': reviews,
            'related_products': related_products,
        }
        return render(request, 'product/product_detail.html', context=context)

    def post(self, request, pk):
        product = Products.objects.get(id=pk)
        if request.method == 'POST':
            if 'delete_review' in request.POST:
                review_id = request.POST.get('delete_review')
                review = Review.objects.get(id=review_id)
                review.delete()
            else:
                comment = request.POST.get('comment')
                star_given = int(request.POST.get('star_given'))
                review = Review.objects.create(
                    comment=comment,
                    star_given=star_given,
                    product=product,
                    user=request.user
                )
                review.save()
        return redirect('products:product-detail', pk=pk)


