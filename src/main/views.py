from django.views.generic import TemplateView, RedirectView
from django.shortcuts import render


class Home(TemplateView):
    template_name = 'index.html'
    extra_context = {
        'page_title': 'home',
        'navbar_title': ''
    }


class About(TemplateView):
    template_name = 'about.html'
    extra_context = {'page_title': 'about'}


class Favicon(RedirectView):
    url = '/static/img/icons/favicon.svg'
    permanent = True


def handler404(request, *args, **kwargs):
    context = {'page_title': '404 error'}
    return render(request, '404.html', context, status=404)


def handler500(request, *args, **kwargs):
    context = {'page_title': '500 error'}
    return render(request, '500.html', context, status=500)