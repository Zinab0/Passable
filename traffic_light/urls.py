from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout, name="logout"),
    path("predict_incident/", views.predict_incident, name="predict_incident"),
    path('get_traffic_information/', views.get_traffic_information, name='get_traffic_information'),
    path('system_check/', views.system_check, name='system_check'),
    path('traffic-info/json/', views.get_traffic_information, name='traffic_info_json'),
    path('traffic-info/', TemplateView.as_view(template_name='traffic_light/traffic_info.html'), name='traffic_info_html'),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)