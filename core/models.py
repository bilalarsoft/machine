from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name="Kategori")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Kategori'

class SeriesCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='series_category')
    name = models.CharField(max_length=100,verbose_name="Seri")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Seri'
        unique_together = (('category', 'name'),)

class ModelCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='model_category')
    series = models.ForeignKey(SeriesCategory, on_delete=models.CASCADE,related_name='model_series_category')
    name = models.CharField(max_length=100,verbose_name="Model Adı")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['series']
        verbose_name_plural = 'Model'


class Product(models.Model):
    name = models.CharField(max_length=100,verbose_name="İsim")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='Kategori',blank=True,null=True)
    series = models.ForeignKey(SeriesCategory,on_delete=models.CASCADE,related_name='Seri',blank=True,null=True)
    model = models.ForeignKey(ModelCategory,on_delete=models.CASCADE,related_name='Model',blank=True,null=True)
    width = models.FloatField(verbose_name="Genişlik Ölçüsü" ,help_text="cm cinsinden genişlik")
    height = models.FloatField(verbose_name="Yükseklik Ölçüsü", help_text="cm cinsinden genişlik")
    depth = models.FloatField(verbose_name="Derinlik Ölçüsü",help_text="cm cinsinden genişlik")
    description = CKEditor5Field('Açıklama', config_name='extends')
    stock = models.IntegerField(verbose_name="Stok Adedi")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Ürünler'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to="product_images/",verbose_name='Fotoğraf')
    alt_text = models.CharField(max_length=100,blank=True,null=True,verbose_name="Fotoğraf Alt Başlığı")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Product Image'


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='video')
    video = models.FileField(upload_to="product_videos/",blank=True,null=True,verbose_name='Video')
    alt_text = models.CharField(max_length=100,blank=True,null=True,verbose_name='Video Alt Başlığı')
    created_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ['-created_date']



