import datetime
from time import strptime
from typing import Callable

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, FormView, DeleteView

from lavanderia.forms import WasherForm, AvaibleSlotForm, ReservedSlotForm
from lavanderia.models import Washer, AvaibleSlot, ReservedSlot


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
    success_url = "/bolsista/washers/"
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
            w_form.save()
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
    template_name = "lavanderia/washer_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Adiciona o formulário ao contexto
        context['washer_form'] = WasherForm()
        return context


class WasherDeleteView(DeleteView):
    model = Washer
    success_url = reverse_lazy("washer_list")


# ---------__TIME SLOT____--------

class TimeSlotDeleteView(DeleteView):
    model = AvaibleSlot
    success_url = reverse_lazy('time_slot_list')


class TimeSlotFormView(FormView):
    model = AvaibleSlot
    form_class = AvaibleSlotForm
    success_url = reverse_lazy('time_slot_list')
    template_name = "lavanderia/avaibleslot_list.html"

    def post(self, request, *args, **kwargs):
        slot_id = self.kwargs.get("pk")
        if slot_id is not None:
            try:
                Slot = AvaibleSlot.objects.get(id=slot_id)
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR,
                                     "A identificador passado como parâmetro não coressponder a nenhum objeto")
                return render(request, template_name=self.template_name)
        else:
            Slot = AvaibleSlot()

        s_form = self.form_class(request.POST, instance=Slot)
        if s_form.is_valid():
            s_form.save()
            messages.success(request, "Salvo com sucesso!")
            return self.form_valid(s_form)
        else:
            return self.form_invalid(s_form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = AvaibleSlot.objects.all()  # Adiciona todos os Washers ao contexto
        return context


class AvaibleSlotListView(ListView):
    model = AvaibleSlot
    form_class = AvaibleSlotForm
    paginate_by = 100
    template_name = "lavanderia/avaibleslot_list.html"

    def get_context_data(self, **kwargs):
        self.object = []
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context


class BaseCRUDView(View):
    list_view: View | None = None
    delete_view: View | None = None
    form_view: View | None = None
    form: Callable = None

    def get(self, request, *args, **kwargs):
        view = self.list_view.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('_method') == 'delete':
            delete_view = self.delete_view.as_view()
            return delete_view(request, *args, **kwargs)

        # Processa o formulário de Washer
        form_view = self.form_view.as_view()
        form_response = form_view(request, *args, **kwargs)

        # Verifica se o formulário é válido ou contém erros
        if form_response.status_code == 302:
            # Se o formulário foi bem-sucedido, redireciona ou exibe a lista atualizada
            return form_response  # Redireciona ao sucesso

        # Se houver erros no formulário, precisamos exibir a lista de Washers junto com os erros
        list_view = self.list_view.as_view()
        rget = request
        rget.method = 'GET'
        list_response = list_view(request, *args, **kwargs)

        # Pega o contexto da lista
        list_context = list_response.context_data

        # Insere o formulário com erros no contexto
        if hasattr(form_response, 'context_data') and 'form' in form_response.context_data:
            list_context['form'] = form_response.context_data['form']  # Formulário com erros
        else:
            list_context['form'] = self.form()  # Formulário vazio se não houver erros

        # Adiciona as mensagens ao contexto
        list_context['messages'] = messages.get_messages(request)

        # Renderiza a resposta final, unindo a lista com o formulário
        return render(request, self.list_view.template_name, list_context)


class WasherListCreateView(StaffRequireBolsista, BaseCRUDView):
    form_view = WasherFormView
    form = WasherForm
    list_view = WasherListView
    delete_view = WasherDeleteView


# FIXME Decida TimeSlot ou AvaiableSlot
class AvaibleSlotView(BaseCRUDView):
    form_view = TimeSlotFormView
    form = AvaibleSlotForm
    list_view = AvaibleSlotListView
    delete_view = TimeSlotDeleteView


# Agendamentos

class AgendamentoDeleteView(DeleteView):
    model = Washer
    success_url = reverse_lazy("agendamentos_view")


class AgendamentoListView(ListView):
    model = ReservedSlot
    form_class = ReservedSlotForm
    paginate_by = 100
    template_name = "lavanderia/agendamento_list.html"

    def get_queryset(self):
        # Acessando os parâmetros da URL (por exemplo: ?start_date=2024-01-01)
        start_date = self.request.GET.get('start', None)

        # Se 'start_date' foi passado, converte para um objeto DateTime
        if start_date:
            start_date = strptime(start_date, "%Y-%m-%d")
        else:
            start_date = datetime.date.today()  # Se não for passado, filtra a partir da data atual

        # Retorna o queryset filtrado pela data
        return ReservedSlot.objects.filter(date__gte=start_date).order_by('date')


class AgendamentoFormView(FormView):
    pass  # TODO


class AgendamentosView(BaseCRUDView):
    form_view = AgendamentoFormView
    form = ReservedSlotForm
    list_view = AgendamentoListView
    delete_view = AgendamentoDeleteView


# Parte dos usuarios comuns

class AvailableSlotListView(ListView):
    model = AvaibleSlot
    template_name = 'lavanderia/usuario/available_slot_list.html'  # Seu template aqui
    context_object_name = 'available_slots'
    paginate_by = 10  # Número de slots por página

    def get_queryset(self):
        # Pega a data e hora atual
        current_time = timezone.now()

        # Seleciona os AvaibleSlots que começam a partir do momento atual e não estão reservados
        queryset = AvaibleSlot.objects.filter(
            #      start__gte=current_time  # Slots com data e hora de início futura
        ).exclude(
            id__in=ReservedSlot.objects.values_list('slot_id', flat=True)  # Exclui slots já reservados
        ).order_by('start')  # Ordena os slots por data de início

        return queryset


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from lavanderia.models import AvaibleSlot, ReservedSlot


@login_required
def schedule_slot(request, pk):
    slot = get_object_or_404(AvaibleSlot, pk=pk)

    # Verifica se o slot já foi reservado
    if ReservedSlot.objects.filter(slot=slot).exists():
        # Redireciona ou exibe uma mensagem informando que o slot já foi reservado
        messages.add_message(request, messages.ERROR,
                             "Horário já agendado")
        return redirect('horarios')

    # Cria a reserva para o usuário logado
    ReservedSlot.objects.create(slot=slot, user=request.user)

    # Redireciona após agendamento (pode ser para uma página de confirmação)
    return redirect('meus_agendamentos')



class UserReservationListView(LoginRequiredMixin, ListView):
    model = ReservedSlot
    template_name = "lavanderia/usuario/agendamentos.html"
    context_object_name = "reservations"

    def get_queryset(self):
        # Filtra os agendamentos do usuário logado
        return ReservedSlot.objects.filter(user=self.request.user)

class ReservationCancelView(LoginRequiredMixin, DeleteView):
    model = ReservedSlot
    success_url = reverse_lazy('meus_agendamentos')  # Redireciona para a lista de reservas após cancelar

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Agendamento cancelado com sucesso.")
        return super().delete(request, *args, **kwargs)
