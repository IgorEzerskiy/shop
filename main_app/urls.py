from django.urls import path, include

urlpatterns = [
    path('api/', include('main_app.api.urls'))
]
