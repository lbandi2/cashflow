from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.http import request, HttpResponseRedirect

from datetime import datetime, timedelta

from cashflow.models import OperationCategories, Keyword
from .forms import EditCatForm, AddKwForm

class RedirectToPreviousMixin:
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']


class CatEditView(LoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    template_name = 'categories/edit_cat.html'
    form_class = EditCatForm
    model = OperationCategories

    def get_context_data(self):
        context = super(CatEditView, self).get_context_data()
        context["obj"] = self.object
        context["title"] = "Edit item"
        context["form2"] = AddKwForm
        return context


# class CatDeleteView(LoginRequiredMixin, DeleteView):
#     template_name = 'categories/delete.html'
#     model = OperationCategories
#     success_url = reverse_lazy('categories:index')

def remove_category(request, **kwargs):
    category = OperationCategories.objects.get(pk=kwargs['pk'])
    category.delete()
    return redirect('categories:index')


class CatIndexView(LoginRequiredMixin, ListView):
    template_name = 'categories/index.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        return OperationCategories.objects.all().order_by('name')


class CatAddView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):
    template_name = 'categories/add.html'
    model = OperationCategories
    login_url = 'home:login'
    fields = ["name"]

    def get_context_data(self):
        context = super(CatAddView, self).get_context_data()
        context["title"] = "Agregar categoría"
        return context


class KwIndexView(LoginRequiredMixin, ListView):
    template_name = 'keywords/index.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        queryset = Keyword.objects.all()
        return queryset


class KwAddView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):
    template_name = 'categories/add_kw.html'
    login_url = 'home:login'
    model = Keyword
    form_class = AddKwForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.name = self.object.name.lower()
        self.object.category = OperationCategories.objects.get(pk=self.kwargs['pk'])
        self.object = form.save()
        return redirect('categories:edit', pk=self.object.category.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['category'] = OperationCategories.objects.get(id=self.kwargs["pk"])
        return context

# def add_keyword(request, **kwargs):
#     print(kwargs)
#     # print(request.method)
#     # print(request)
#     category = OperationCategories.objects.get(pk=kwargs['pk'])
#     keyword = Keyword(name=kwargs['kw_name'], category=category)
#     keyword.save()
#     return redirect('categories:edit', pk=kwargs['pk'])

# class KwAddView(LoginRequiredMixin, RedirectToPreviousMixin, CreateView):
#     template_name = 'categories/add_kw.html'
#     form_class = AddKwForm
#     model = Keyword

#     def get_context_data(self):
#         context = super(KwAddView, self).get_context_data()
#         context["obj"] = self.object
#         return context

#     def form_valid(self, form):
#         # self.object = form.save()
#         print("form", form.cleaned_data)
#         self.object = form.save(commit=False)
#         self.object.name = self.object.name.lower()
#         self.object.category = OperationCategories.objects.get(pk=self.kwargs['pk'])
#         self.object = form.save()
#         return redirect('categories:edit', pk=self.object.category.id)


def remove_keyword(request, **kwargs):
    keyword = Keyword.objects.get(pk=kwargs['kw'])
    keyword.delete()
    return redirect('categories:edit', pk=kwargs['pk'])
