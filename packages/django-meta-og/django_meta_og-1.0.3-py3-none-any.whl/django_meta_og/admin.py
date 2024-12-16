from django.contrib import admin

from .models import Content, Namespace, Property


@admin.register(Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    ordering = ["prefix"]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    ordering = ["namespace", "name"]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    ordering = ["property", "content"]
