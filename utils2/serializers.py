from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Todo


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]

    # if we dont override create method , the default create  method will allow duplicate entries

    def create(self, validated_data):
        """
        Overriding the create method to handle user creation.
        We're now using Django's get_or_create method to either create a new user or return an existing one.
        """

        password = validated_data.pop("password")  # Remove password from validated_data
        user, created = User.objects.get_or_create(
            email=validated_data["email"],
            defaults={
                "username": validated_data["username"],
                "first_name": validated_data.get("first_name", ""),
                "last_name": validated_data.get("last_name", ""),
            },
        )

        if created:
            # Hash the password and save the user
            user.set_password(password)
            user.save()

        return user  # Return the user instance


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            "id",
            "title",
            "is_completed",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id"]  # read only

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
