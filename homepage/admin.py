# homepage/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.db import models            # <-- DB alan tipi buradan
from django.forms import Textarea        # <-- Widget buradan

from .models import Hero_section, About_section, Statistics_area, Our_values, Faq, Business_partner

class CompactTextareaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4})}
    }



# =======================
# 1) HERO SECTION (landing/hero alanı)
# =======================
@admin.register(Hero_section)
class HeroSectionAdmin(CompactTextareaAdmin):
    list_display = ("title", "youtube_url", "image_preview")
    search_fields = ("title", "description", "youtube_url")
    ordering = ("title",)
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Metin", {
            "fields": ("title", "description")
        }),
        ("Medya", {
            "fields": ("image", "youtube_url")
        }),
    )

    @admin.display(description="Önizleme")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px;border-radius:6px;" />', obj.image.url)
        return "—"

    # Bu alan genelde tek kayıtla yönetilir; istersen eklemeyi 1 kayıtla sınırla:
    def has_add_permission(self, request):
        if Hero_section.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


# =======================
# 2) ABOUT SECTION (Hakkında)
# =======================
@admin.register(About_section)
class AboutSectionAdmin(CompactTextareaAdmin):
    list_display = ("header", "sub_header", "image_preview")
    search_fields = ("header", "sub_header", "home_description", "detail_description")
    ordering = ("header",)
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Başlıklar", {"fields": ("header", "sub_header")}),
        ("Kısa Açıklama (Ana Sayfa)", {"fields": ("home_description",)}),
        ("Detay Açıklama", {"fields": ("detail_description",)}),
        ("Görsel", {"fields": ("image", "image_preview")}),
    )

    @admin.display(description="Önizleme")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px;border-radius:6px;" />', obj.image.url)
        return "—"


# =======================
# 3) STATISTICS (Sayaçlar) — genelde tek kayıt
# =======================
@admin.register(Statistics_area)
class StatisticsAreaAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'icon')  # listede görünecek sütunlar
    search_fields = ('title',)                 # başlığa göre arama
    list_filter = ('title',)                   # filtreleme (isteğe bağlı)
    ordering = ('title',)                      # alfabetik sıralama
    list_editable = ('value', 'icon')          # listedeyken düzenlenebilsin

# =======================
# 4) OUR VALUES (Değerlerimiz)
# =======================
@admin.register(Our_values)
class OurValuesAdmin(CompactTextareaAdmin):
    list_display = ("title", "short_description", "image_preview")
    search_fields = ("title", "description")
    ordering = ("title",)
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("İçerik", {"fields": ("title", "description")}),
        ("Görsel", {"fields": ("image", "image_preview")}),
    )

    @admin.display(description="Özet")
    def short_description(self, obj):
        return (obj.description[:60] + "…") if obj.description and len(obj.description) > 60 else obj.description

    @admin.display(description="Önizleme")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', obj.image.url)
        return "—"


# =======================
# 5) FAQ (Sık Sorulanlar)
# =======================
@admin.register(Faq)
class FaqAdmin(CompactTextareaAdmin):
    list_display = ("short_question", "short_answer")
    search_fields = ("question", "answer")
    ordering = ("question",)

    @admin.display(description="Soru")
    def short_question(self, obj):
        return (obj.question[:70] + "…") if obj.question and len(obj.question) > 70 else obj.question

    @admin.display(description="Cevap")
    def short_answer(self, obj):
        return (obj.answer[:70] + "…") if obj.answer and len(obj.answer) > 70 else obj.answer

@admin.register(Business_partner)
class BusinessPartnerAdmin(CompactTextareaAdmin):
    list_display = ("name","img_alt")
    search_fields = ("name",)
    ordering = ("name",)

    @admin.display(description="Önizleme")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px;border-radius:6px;" />', obj.image.url)
        return "—"
