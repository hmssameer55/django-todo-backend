from django.urls import path
from .views import RegisterUserView, TodoView, TodoDetailView


urlpatterns = [
    path("register/", RegisterUserView.as_view()),
    path("todo/", TodoView.as_view()),
    path("todo/<int:pk>/", TodoDetailView.as_view()),
]
