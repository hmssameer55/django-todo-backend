from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_completed", "description", "user")
    search_fields = ("title", "description")
    fields = (
        "title",
        "is_completed",
        "description",
    )  # Ensure user field is editable if required


# Register the Todo model with the custom admin class
admin.site.register(Todo, TodoAdmin)
