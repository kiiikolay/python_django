"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.д.
"""
import json
from pickle import FALSE
from timeit import default_timer
from csv import DictWriter

from django.core.cache import  cache
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views import View
# from django.contrib.auth import authenticate, login, logout
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.syndication.views import Feed


from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser
from yaml import serialize

from .common import save_csv_products, save_csv_orders
from .models import Product, Order, ProductImage
from .forms import ProductForm, OrderForm, GroupForm
from .serializers import ProductSerializer, OrderSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse

class LatestProductsFeed(Feed):
    title = "Блог продуктов"
    description = "Изменения поступают в блок когда вы изменяете содержимое или создаёте новые продукты"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return (
            Product.objects
                .select_related("created_by").all()
                .filter(archived=False)
                .order_by("-create_at")[:5]
    )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]

@extend_schema(description="Product view CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]

    @method_decorator(cache_page(60 * 2))
    def list(self, *args, **kwargs):
        # print("hello products list")
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Get one product by ID",
        description="Retrive **product**, returns 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty response, product by id not found"),
        }
    )
    @action(methods="get", detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attchment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response

    @action(
        detail=False,
        methods=["post"],
        parser_classes=[MultiPartParser],
    )
    def uploap_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ["products"]
    filterset_fields = [
        "deliveri_address",
        "promocode",
        "user",
        "products",
    ]
    ordering_fields = [
        "deliveri_address",
        "products",
        "create_at",
    ]

    def perform_create(self, serializer):
        # Получаем текущего пользователя из запроса
        user = self.request.user
        # Сохраняем объект, передавая текущего пользователя в поле created_by
        serializer.save(created_by=user)

    def perform_update(self, serializer):
        # Получаем текущего пользователя из запроса
        user = self.request.user
        # Сохраняем объект, передавая текущего пользователя в поле updated_by
        serializer.save(updated_by=user)

    @action(methods="get", detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = "orders-export.csv"
        response["Content-Disposition"] = f"attchment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "deliveri_address",
            "promocode",
            "user",
            "products",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for order in queryset:
            writer.writerow({
                field: getattr(order, field)
                for field in fields
            })

        return response

    @action(
        detail=False,
        methods=["post"],
        parser_classes=[MultiPartParser],
    )
    def uploap_csv(self, request: Request):
        orders = save_csv_orders(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

@api_view()
def api_hello_view(request: Request) -> Response:
    return Response({"message": "Hello!"})

class ShopIndexView(View):

    # @method_decorator(cache_page(60 * 2))
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999)
        ]

        context = {
            "time_running": default_timer(),
            "products": products,
            "items": 3,
        }
        print("shop index context", context)
        return render(request, 'shopapp/shop-index.html', context=context)

class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return  render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)

"""______________________PRODUCTS____________________________"""

class ProductDetailsView(DetailView):
    template_name = "shopapp/product-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("image")
    context_object_name = "product"

class ProductsListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

# def products_list(request: HttpRequest):
#     context = {
#         "products": Product.objects.all(),
#     }
#     return render(request, 'shopapp/products-list.html', context=context)

class ProductCreateView(PermissionRequiredMixin, CreateView):
    # def test_func(self):
        # return self.request.user.groups.filter(name="secret-group").exists()
        # return self.request.user.is_superuser
    permission_required = "shopapp.add_product"
    model = Product
    fields = "name", "description", "price", "discount", "preview"
    # form_class = ProductForm
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return Product.created_by == self.request.user.pk
#     fields = "name", "description", "price", "discount", "preview"
    form_class = ProductForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")
    template_name_suffix = "_confirm_archive"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived
                }
                for product in products
            ]

            cache.set(cache_key, products_data, 300)

        return JsonResponse({"products": products_data})

"""______________________ORDERS___________________________"""

class OrderCreateView(CreateView):
    template_name = "shopapp/create-order.html"
    model = Order
    fields = "deliveri_address", "promocode", "user", "products"
    success_url = reverse_lazy("shopapp:orders_list")

class OrdersListViev(LoginRequiredMixin ,ListView):
    queryset = (Order.objects
                .select_related("user")
                .prefetch_related('products').all()
    )


class UserOrdersListView(LoginRequiredMixin ,ListView):
    model = Order
    template_name = "shopapp/order_list.html"
    context_object_name = 'orders'


    def get_queryset(self):
        self.owner = get_object_or_404(User, pk=self.kwargs["user_id"])
        return Order.objects.filter(user=self.owner).prefetch_related('products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context

class OrdersDetailViev(PermissionRequiredMixin, DetailView):
    permission_required = "view_order"
    queryset = (Order.objects
                .select_related("user")
                .prefetch_related('products').all()
    )

class OrderUpdateView(UpdateView):
    model = Order
    fields = "deliveri_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )

class OrderDeleteView(DeleteView):

    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

def user_orders_export(request, user_id):
    cache_key = f"user_orders_export_{user_id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(json.loads(cached_data), safe=False)

    try:
        i_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponseNotFound("User not found")

    orders = Order.objects.filter(user=i_user).order_by('pk')
    serializer = OrderSerializer(orders, many=True)
    data = serializer.data

    # Кешируем сериализованные данные
    cache.set(cache_key, json.dumps(data, cls=DjangoJSONEncoder), 300)  # Кэш на 5 минут
    return JsonResponse(data, safe=False)