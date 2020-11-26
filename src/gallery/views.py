from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.db import transaction
from django.db.models import Q

from gallery import models
from gallery import forms

class PetList(ListView):
    model = models.Pet
    extra_context = {'page_title': 'animals'}
    ordering = '-id'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        sort_by = request.GET.get('sort')
        if sort_by:
            self.object_list = models.Pet.objects.all().order_by(
                '-' + sort_by
            )
            self.paginate_by = None
            context = self.get_context_data()
            context['sorted_by'] = sort_by
            return self.render_to_response(context)

        search_query = request.GET.get('search')
        if search_query:
            self.object_list = models.Pet.objects.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(gender__icontains=search_query) |
                Q(category__icontains=search_query)
            ).order_by(self.ordering)
            self.paginate_by = None
            context = self.get_context_data()
            context['search_query'] = search_query
            return self.render_to_response(context)

        return super().get(self, request, *args, **kwargs)


class PetDetail(DetailView):
    model = models.Pet
    extra_context = {'page_title': 'animals'}

    def get(self, request, *args, **kwargs):
        self.extra_context['last_page'] = request.META.get(
            'HTTP_REFERER', reverse('gallery:home')
        )
        if '/create/' in self.extra_context['last_page']:
            self.extra_context['last_page'] = reverse('gallery:home')

        return super().get(request, *args, **kwargs)


class PetCreate(CreateView):
    model = models.Pet
    form_class = forms.PetForm
    extra_context = {
        'page_title': 'animals',
        'navbar_title': 'creating application'
    }

    def get(self, request, *args, **kwargs):
        self.extra_context['last_page'] = request.META.get(
            'HTTP_REFERER', reverse('gallery:home')
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        print(request.POST, request.FILES, sep='\n')
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['photo'] = forms.PetFormset(
                self.request.POST, self.request.FILES
            )
        else:
            data['photo'] = forms.PetFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        photos = context.get('photo')

        with transaction.atomic():
            form.instance.created_by = self.request.user
            if not photos.is_valid():
                return self.form_invalid(form)
            self.object = form.save()
            photos.instance = self.object
            photos.save()

        return HttpResponseRedirect(
            reverse_lazy('gallery:pet-detail', args=(self.object.pk,))
        )