from django.db import models

class Hero_section(models.Model):
    title = models.CharField(max_length=100, verbose_name="Başlık")
    description = models.TextField(verbose_name='Açıklama')
    image = models.ImageField(upload_to='home_page_images', verbose_name='Fotoğraf')
    youtube_url = models.URLField(verbose_name='Youtube URL')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Ana Bölüm'
        verbose_name_plural = 'Ana Bölüm'  # İstersen 'Ana Bölümler' yap

class About_section(models.Model):
    header = models.CharField(max_length=100, verbose_name='Üst Başlık')
    sub_header = models.CharField(max_length=100, verbose_name='Alt Başlık')
    home_description = models.TextField(verbose_name='Ana Sayfa Açıklaması')
    detail_description = models.TextField(verbose_name='Detaylı Açıklama')  # yazım düzeltildi
    image = models.ImageField(verbose_name='Fotoğraf')

    def __str__(self):
        return self.header

    class Meta:
        ordering = ['header']
        verbose_name = 'Hakkında'
        verbose_name_plural = 'Hakkında'  # veya 'Hakkında Bölümleri'

# models.py
class Statistics_area(models.Model):
    title= models.CharField(max_length=100, verbose_name='Başlık')
    value = models.IntegerField(verbose_name='Değer')
    icon  = models.CharField(max_length=100, verbose_name='İkon')


    def __str__(self):
        return f"Başlık:{self.title} / Değer:{self.value}"

    class Meta:
        ordering = ['title']   # <-- düzeltme
        verbose_name = 'İstatistik'
        verbose_name_plural = 'İstatistikler'

class Our_values(models.Model):
    title = models.CharField(max_length=100, verbose_name="Başlık")
    description = models.TextField(verbose_name='Açıklama')
    image = models.ImageField(verbose_name='Fotoğraf')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Değerlerimiz'
        verbose_name_plural = 'Değerlerimiz'

class Faq(models.Model):
    question = models.TextField(verbose_name='Soru')
    answer = models.TextField(verbose_name='Cevap')

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['question']
        verbose_name = "Sık Sorulan Soru"
        verbose_name_plural = 'Sık Sorulan Sorular'

class Business_partner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Firma İsmi")
    image = models.ImageField(upload_to='business_partner', verbose_name='Fotoğraf')
    img_alt = models.CharField(max_length=100,verbose_name="Fotoğraf Alt Etiketi")

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Çalıştığım Firmalar'
