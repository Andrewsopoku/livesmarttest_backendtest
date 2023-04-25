from django.urls import path
from bloodtests.views import BloodTestView

urlpatterns = [
    path('test/<str:code>', BloodTestView.as_view()),
]
