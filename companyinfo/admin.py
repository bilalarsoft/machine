# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count

from .models import Company, Branch, BranchPhoneNumber, Address


# ==========================
# 📞 Inline Yapıları
# ==========================
# Inline yapılar, bir modelin alt ilişkili modellerini (ForeignKey ile bağlı olanları)
# aynı sayfa üzerinde düzenlememizi sağlar.
# Örneğin: Şube (Branch) sayfasında şubeye ait telefonları görebilmek gibi.


class BranchPhoneNumberInline(admin.TabularInline):
    """
    Şube sayfasında alt alta telefon numaralarını tablo şeklinde gösterir.
    """
    model = BranchPhoneNumber
    extra = 1  # Yeni kayıt eklemek için 1 boş satır göster
    fields = ("name", "phone_number")  # Görünen alanlar
    show_change_link = True  # Her telefon kaydına ayrı sayfada gitme linki


class BranchInline(admin.TabularInline):
    """
    Firma (Company) detay sayfasında, o firmaya bağlı şubeleri listelemek için.
    """
    model = Branch
    extra = 0  # Yeni satır eklemeden sadece mevcut olanları göster
    fields = (
        "name",
        "email",
        "is_main",
        "instagram_url",
        "facebook_url",
        "twitter_url",
        "google_business_url",
        "youtube_url",
    )
    show_change_link = True  # Her şubeye gitmek için link oluşturur


# ==========================
# 🏢 Firma Admin
# ==========================
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Firma modelini admin panelinde nasıl göstereceğimizi belirler.
    """
    list_display = (
        "name",
        "phone",
        "mail_address",
        "branch_count",  # Firma kaç şubeye sahip?
        "created",
        "updated",
    )
    search_fields = ("name", "phone", "mail_address")  # Arama yapılabilecek alanlar
    list_filter = ("created", "updated")  # Sağda filtreleme menüsü
    readonly_fields = ("created", "updated")  # Bu alanlar sadece görüntülenir
    inlines = [BranchInline]  # Firma detayında şubeleri göster
    ordering = ("name",)  # Liste sıralaması

    def get_queryset(self, request):
        """
        Liste görünümünde şube sayısını tek sorguda hesaplar (performans artışı).
        """
        qs = super().get_queryset(request)
        return qs.annotate(branch_count=Count("branch"))

    @admin.display(description="Şube Sayısı", ordering="branch_count")
    def branch_count(self, obj):
        """
        Firma kaç şubeye sahip, listede gösterir.
        """
        return obj.branch_count


# ==========================
# 🏬 Şube Admin
# ==========================
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """
    Şube modelinin admin paneli görünümü.
    """
    list_display = (
        "name_with_star",  # Ana şube ise yıldızla göster
        "company",  # Hangi firmaya bağlı
        "email",
        "is_main",
        "phones_count",  # Kaç telefon numarası var
        "created",
        "updated",
        "photo_preview",  # Görsel önizleme
    )
    list_select_related = ("company",)  # Firma bilgilerini önceden getirir (performans)
    search_fields = ("name", "email", "company__name", "address")  # Arama alanları
    list_filter = ("company", "is_main", "created", "updated")  # Filtre menüsü
    readonly_fields = ("created", "updated", "photo_preview")  # Sadece görüntülenecek alanlar
    ordering = ("name",)
    inlines = [BranchPhoneNumberInline]  # Şube sayfasında telefon numaralarını göster

    # Alanları düzenli gruplar halinde göstermek için fieldset kullanıyoruz.
    fieldsets = (
        ("Temel Bilgiler", {
            "fields": ("company", "name", "email", "is_main"),
        }),
        ("Adres & Görsel", {
            "fields": ("address", "photo"),
        }),
        ("Sosyal Medya", {
            "fields": (
                "instagram_url",
                "facebook_url",
                "twitter_url",
                "google_business_url",
                "youtube_url",
            )
        }),
        ("Sistem", {
            "classes": ("collapse",),  # Bu grup gizlenebilir olacak
            "fields": ("created", "updated"),
        }),
    )

    @admin.display(description="Şube", ordering="name")
    def name_with_star(self, obj):
        """
        Ana şubeleri yıldızla vurgulamak için.
        """
        return f"{obj.name} {'⭐' if obj.is_main else ''}"

    def get_queryset(self, request):
        """
        Telefon sayısını annotate ederek tek sorguda hesaplar.
        """
        qs = super().get_queryset(request)
        return qs.annotate(_phones_count=Count("phones"))

    @admin.display(description="Telefon Adedi", ordering="_phones_count")
    def phones_count(self, obj):
        """
        Şubeye ait telefon sayısını listede gösterir.
        """
        return obj._phones_count

    @admin.display(description="Önizleme")
    def photo_preview(self, obj):
        """
        Fotoğraf alanını küçük bir önizleme olarak gösterir.
        """
        if obj.photo:
            return format_html('<img src="{}" style="max-height:80px; border-radius:6px;" />', obj.photo.url)
        return "—"  # Eğer fotoğraf yoksa boş çizgi göster


# ==========================
# ☎️ Şube Telefon Numaraları Admin
# ==========================
@admin.register(BranchPhoneNumber)
class BranchPhoneNumberAdmin(admin.ModelAdmin):
    """
    Şubelere bağlı telefon numaralarının yönetimi.
    """
    list_display = ("branch", "name", "phone_number", "created_at", "updated_at")
    list_select_related = ("branch",)
    search_fields = ("name", "phone_number", "branch__name", "branch__company__name")
    list_filter = ("branch__company", "branch", "created_at", "updated_at")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")


# ==========================
# 📍 Adres Admin
# ==========================
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Adres modelinin admin paneli görünümü.
    """
    list_display = ("short_address", "province", "district", "created_at", "updated_at")
    search_fields = ("address", "province", "district")
    list_filter = ("province", "district", "created_at", "updated_at")
    ordering = ("address",)
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Adres")
    def short_address(self, obj):
        """
        Adres çok uzunsa liste görünümünde kısaltır.
        """
        return (obj.address[:60] + "…") if len(obj.address) > 60 else obj.address
