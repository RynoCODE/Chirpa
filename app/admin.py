from django.contrib import admin
from .models import Question

# Register your models here.
class questionsAdmin(admin.ModelAdmin):
    list_display = ['text', 'user', 'created_at', 'updated_at']
admin.site.register(Question, questionsAdmin)