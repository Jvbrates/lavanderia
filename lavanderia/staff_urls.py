from django.urls import path
from lavanderia.views import WasherListCreateView, AvaibleSlotView, WasherDeleteView, AgendamentosView, \
    ReservedSlotListView

urlpatterns = [
    path('washers/', WasherListCreateView.as_view(), name='washer_list'),  # CREATE E LIST
    path('washers/<int:pk>', WasherListCreateView.as_view(), name='washer_update_delete'),  # UPDATE E DELETE

    path('timeslots/', AvaibleSlotView.as_view(), name="time_slot_list"), # CREATE E LIST
    path('timeslots/<int:pk>', AvaibleSlotView.as_view(), name="time_update_delete"), # UPDATE e DELETE

    path('agendamentos/', ReservedSlotListView.as_view(), name='reserved_slots'),
]
