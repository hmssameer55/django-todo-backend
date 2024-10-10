from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, TodoSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Todo


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()
        user = User.objects.get(username=serializer.data["username"])
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status=201)


class TodoView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    query_set = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        # Fetch only the todos for the authenticated user
        return Todo.objects.filter(user=self.request.user)


class TodoDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    query_set = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        # Fetch only the todos for the authenticated user
        return Todo.objects.filter(user=self.request.user)
