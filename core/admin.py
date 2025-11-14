from django.contrib import admin
from django.forms import BaseInlineFormSet

from .models import Category, SeriesCategory, ModelCategory, Product, ProductImage, ProductVideo


# ======================
# Inline Görünümler
# ======================
class ProductImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        cover_count = 0
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                continue
            if form.cleaned_data.get('is_cover'):
                cover_count += 1
        if cover_count > 1:
            from django.core.exceptions import ValidationError
            raise ValidationError("Bir üründe yalnızca 1 kapak görseli seçebilirsiniz.")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text','is_cover')
    verbose_name = "Ürün Görseli"
    verbose_name_plural = "Ürün Görselleri"
    formset = ProductImageInlineFormSet


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 0
    fields = ('video', 'alt_text')
    verbose_name = "Ürün Videosu"
    verbose_name_plural = "Ürün Videoları"


# ======================
# Ürün Admini
# ======================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductVideoInline]

    list_display = ('name', 'category', 'series', 'model', 'stock', 'updated')
    list_filter = ('category', 'series', 'model')
    search_fields = ('name', 'category__name', 'series__name', 'description')
    readonly_fields = ('created', 'updated')

    fieldsets = (
        ("Ürün Bilgileri", {
            'fields': ('name', 'category', 'series', 'model', 'description')
        }),
        ("Ölçüler ve Stok", {
            'fields': ('width', 'height', 'depth', 'stock')
        }),
        ("Zaman Bilgileri", {
            'fields': ('created', 'updated')
        }),
    )


# ======================
# Kategori / Seri / Model Adminleri
# ======================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')
    search_fields = ('name',)
    ordering = ('name',)
    verbose_name = "Kategori"
    verbose_name_plural = "Kategoriler"


@admin.register(SeriesCategory)
class SeriesCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created', 'updated')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    ordering = ('category', 'name')
    verbose_name = "Seri"
    verbose_name_plural = "Seriler"


@admin.register(ModelCategory)
class ModelCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'series', 'created', 'updated')
    list_filter = ('series', 'series__category')
    search_fields = ('name', 'series__name', 'series__category__name')
    ordering = ('series', 'name')
    verbose_name = "Model"
    verbose_name_plural = "Modeller"


# ======================
# Görsel ve Video Adminleri (isteğe bağlı)
# ======================

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'created')
    list_filter = ('product',)
    search_fields = ('product__name',)
    ordering = ('product',)


@admin.register(ProductVideo)
class ProductVideoAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'created_date')
    list_filter = ('product',)
    search_fields = ('product__name',)
    ordering = ('product', '-created_date')
