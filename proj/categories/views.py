from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from datetime import datetime, timedelta

from cashflow.models import OperationCategories
from .forms import EditCatForm

class CatEditView(LoginRequiredMixin, UpdateView):
    template_name = 'categories/edit_cat.html'
    form_class = EditCatForm
    model = OperationCategories

    def get_context_data(self):
        context = super(CatEditView, self).get_context_data()
        context["obj"] = self.object
        context["title"] = "Edit item"
        return context
    
    def get_success_url(self):
        return reverse("categories:index")


class CatIndexView(LoginRequiredMixin, ListView):
    template_name = 'categories/index.html'
    login_url = 'home:login'
    context_object_name = 'item_list'

    def get_queryset(self):
        return OperationCategories.objects.all()


class CatAddView(LoginRequiredMixin, CreateView):
    template_name = 'categories/add.html'
    model = OperationCategories
    login_url = 'home:login'
    fields = ["name"]

    def get_success_url(self):
        return reverse("categories:index")

    def get_context_data(self):
        context = super(CatAddView, self).get_context_data()
        context["title"] = "Agregar categoría"
        return context