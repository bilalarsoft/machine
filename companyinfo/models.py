from django.core.validators import RegexValidator
from django.db import models, transaction
from django.db.models import Q

# Create your models here.

phone_validator = RegexValidator(
    regex=r'^05\d{9}$',
    message="Telefon numarası 05 ile başlamalı ve 11 haneli olmalı (örnek: 05551234567)."
)
class Company(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Firma İsmi'
    )
    phone = models.CharField(validators=[phone_validator], max_length=11, blank=True,verbose_name='Telefon Numarası')
    whatsapp = models.CharField(max_length=200,verbose_name='Whatsapp Numarası')
    mail_address = models.EmailField(verbose_name='Mail Adresi')
    logo = models.ImageField(upload_to='logos', verbose_name='Logo Girdi')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Firma Bilgisi'
        verbose_name_plural = 'Firma Bilgileri'


class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branch', verbose_name='Firma')
    name = models.CharField(max_length=100,verbose_name='Şube Adı',unique=True)
    email = models.EmailField(verbose_name='E-Mail',unique=True,blank=True,null=True)
    address = models.TextField(verbose_name='Adres',blank=True)
    photo = models.ImageField(upload_to='companyinfo/images/',blank=True,verbose_name='Picture')

    #sosyal medya hesapları
    instagram_url = models.URLField(verbose_name='Instagram URL',blank=True)
    facebook_url = models.URLField(verbose_name='Facebook URL',blank=True)
    twitter_url = models.URLField(verbose_name='Twitter URL',blank=True)
    google_business_url = models.URLField(verbose_name='Google Business URL',blank=True)
    youtube_url = models.URLField(verbose_name='Youtube URL',blank=True)

    #ana şube belirleyici
    is_main = models.BooleanField(default=False,verbose_name='Is Main')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Şube'
        verbose_name_plural = 'Şubeler'
        constraints = [
            models.UniqueConstraint(
                fields=["company"],
                condition=Q(is_main=True),
                name="unique_main_branch_per_company",
            )
        ]
        indexes = [
            models.Index(fields=["company", "is_main"]),
            models.Index(fields=["name"]),
        ]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_main:
                # Önce diğerlerini pasifleştir
                Branch.objects.filter(company=self.company, is_main=True).exclude(pk=self.pk).update(is_main=False)
            super().save(*args, **kwargs)
    def __str__(self):
        badge = " ⭐" if self.is_main else ""
        return f"{self.company.name} - {self.name}{badge}"

class BranchPhoneNumber(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='phones', verbose_name='Şube')
    name = models.CharField(max_length=100,verbose_name="Telefon Sahibi")
    phone_number = models.CharField(max_length=11,validators=[phone_validator],help_text='Telefon numarası 05... ile başlamalıdır.',verbose_name="Telefon Numarası")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.branch.name} - {self.phone_number}"
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Şube Telefon Bilgisi'

class Address(models.Model):
    address = models.TextField(verbose_name="Adres")
    province = models.CharField(verbose_name="İl", max_length=100)
    district = models.CharField(verbose_name='İlçe', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address
    class Meta:
        ordering = ['address']
        verbose_name_plural = 'Adres'