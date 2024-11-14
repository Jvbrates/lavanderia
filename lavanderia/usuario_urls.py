from django.urls import path
from lavanderia.views import WasherListCreateView, AvaibleSlotView, WasherDeleteView, AgendamentosView, \
    AvailableSlotListView, UserReservationListView, ReservationCancelView, schedule_slot

urlpatterns = [
    path('horarios/', AvailableSlotListView.as_view(), name='horarios'),  # LISTA HORARIOS DISPONIVEIS
    path('horarios/<int:pk>', schedule_slot, name='schedule_slot'),  # UPDATE E DELETE

    path('agendamentos/', UserReservationListView.as_view(), name="meus_agendamentos"),  # Listar Agendamentos
    path('agendamentos/<int:pk>', ReservationCancelView.as_view(), name="cancelar_agendamento"),  # Listar Agendamentos
    # path('agendamentos/<int:pk>', AgendamentosView.as_view(), name="agendamentos_delete"),  # UPDATE e DELETE

]
