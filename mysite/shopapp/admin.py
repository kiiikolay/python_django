from io import TextIOWrapper
from csv import DictReader

from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import admin_actions
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm

class OrderInline (admin.TabularInline):
    model = Product.orders.through

class ProductInline(admin.StackedInline):
    model = ProductImage

@admin.action(description="Archive products")
def merk_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description="Unarchive products")
def merk_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = "shopapp/products_changelist.html"

    actions = [
        merk_archived,
        merk_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
        ProductInline
    ]
    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    list_display_links = "pk", "name"
    ordering = "name", "pk"
    search_fields = "name", "description"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide", "collapse"),
        }),
        ("Images", {
            "fields": ("preview", ),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": "Extra options. Field 'arhived' is for soft delete",
        }),
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html")
        form =CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", status=400)

        csv_file = TextIOWrapper(
            form.files["csv_file"].file,
            encoding=request.encoding,
        )

        reader = DictReader(csv_file)

        products = [Product(**row)
                    for row in reader
        ]
        Product.objects.bulk_create(products)
        self.message_user(request, "Data from CSV  was imported")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv"
            )
        ]
        return new_urls + urls




# admin.site.register(Product, ProductAdmin)

# class ProductInline(admin.TabularInline):

class ProductInline(admin.StackedInline):
    model = Order.products.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "deliveri_address", "promocode", "create_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return  obj.user.first_name or obj.user.username


