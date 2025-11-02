from django.shortcuts import render
from homepage.models import *
from companyinfo.models import *
from urllib.parse import urlparse, parse_qs
# Create your views here.

from django.http import HttpResponse


def yt_embed_url(raw_url: str) -> str:
    if not raw_url:
        return ''
    u = urlparse(raw_url)
    host = u.netloc.lower()
    path = u.path

    video_id = ''
    # https://youtu.be/VIDEOID
    if 'youtu.be' in host:
        video_id = path.lstrip('/').split('/')[0]
    # https://www.youtube.com/shorts/VIDEOID
    elif '/shorts/' in path:
        video_id = path.split('/shorts/')[1].split('?')[0]
    # https://www.youtube.com/watch?v=VIDEOID
    else:
        qs = parse_qs(u.query)
        video_id = (qs.get('v') or [''])[0]

    return f'https://www.youtube.com/embed/{video_id}' if video_id else ''
def index(request):
    hero = Hero_section.objects.first()
    context = {
        'hero_section': Hero_section.objects.first(),
        'about_section': About_section.objects.first(),
        'statistic_area': Statistics_area.objects.all(),
        'our_values' : Our_values.objects.first(),
        'faq' : Faq.objects.all(),
        'company' : Company.objects.first(),
        'hero_youtube_embed': yt_embed_url(hero.youtube_url) if hero else '',

    }
    return render(request,'core/index.html',context)
