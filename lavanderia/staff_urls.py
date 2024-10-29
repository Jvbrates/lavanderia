from django.urls import path
from lavanderia.views import WasherListCreateView

urlpatterns = [
    path('washers/', WasherListCreateView.as_view(), name='washer_list'),  # CREATE E LIST
    path('washers/<int:pk>', WasherListCreateView.as_view(), name='washer_list_create'),  # UPDATE E DELETE
    path('timeSlots/', timeSlotView.as_view(), name="time_slot_list"), # CREATE E LIST
    path('timeSlots/', timeSlotView.as_view(), name="time_update_delete"), # UPDATE e DELETE
]
