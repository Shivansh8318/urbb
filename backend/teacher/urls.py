from django.urls import path
from .views import ValidateTokenView

urlpatterns = [
    path('validate-token/', ValidateTokenView.as_view(), name='validate-student-token'),
]