from lavanderia import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bolsista/', include("lavanderia.staff_urls")),
    path('', include("lavanderia.usuario_urls")),
    path("accounts/logout/", views.user_logout, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),

]
