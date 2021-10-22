from django.urls import path
from . import views

app_name = 'conversation'

urlpatterns = [
    path("chatting/<int:a_pk>/<int:b_pk>", views.go_Chatting, name="go"),
    path("<int:pk>", views.ConversationDetailView.as_view(), name="detail"),
]