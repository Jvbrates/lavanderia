from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, FormView
from django.views.generic.list import MultipleObjectMixin

from lavanderia.forms import WasherForm
from django.db.models import ObjectDoesNotExist

from lavanderia.models import Washer
import typing


@login_required
def view_test(request):
    return render(request, "test.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("login", permanent=True)


class StaffRequireBolsista(UserPassesTestMixin):
    login_url = "/"
    raise_exception = True

    def test_func(self):
        return self.request.user.bolsista


# WASHERS

class WasherFormView(FormView):
    model = Washer
    form_class = WasherForm
    success_url = "/"
    template_name = "lavanderia/washer_list.html"

    def post(self, request, *args, **kwargs):
        w_id = self.kwargs.get('pk')
        if w_id is not None:
            try:
                washer = Washer.objects.get(id=w_id)
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR,
                                     "A identificador passado como parâmetro não coressponder a nenhum objeto")
                return render(request, template_name=self.template_name)
        else:
            washer = None

        w_form = self.form_class(request.POST, instance=washer)
        if w_form.is_valid():
            messages.success(request, "Salvo com sucesso!")
            return self.form_valid(w_form)
        else:
            return self.form_invalid(w_form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Washer.objects.all()  # Adiciona todos os Washers ao contexto
        return context


class WasherListView(ListView):
    model = Washer
    form_class = WasherForm
    paginate_by = 100
    success_url = "/"
    template_name = "lavanderia/washer_list.html"

    def get_context_data(self, **kwargs):
        self.object = []  # assign the object to the view
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Adiciona o formulário ao contexto
        return context


class WasherListCreateView(StaffRequireBolsista, View):
    def get(self, request, *args, **kwargs):
        view = WasherListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = WasherFormView.as_view()
        response = view(request, *args, **kwargs)

        # Se houver erros no formulário, junte as mensagens e os erros com a WasherListView
        list_view = WasherListView.as_view()
        context = list_view(request, *args, **kwargs)  # Chama a lista de Washers

        # Adiciona as mensagens ao contexto
        context.context_data['form'] = response.context_data['form']  # Formulário com erros
        context.context_data['messages'] = messages.get_messages(request)  # Captura as mensagens

        return render(request, list_view.template_name, context.context_data)


