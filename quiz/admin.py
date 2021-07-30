from django.contrib import admin
from .models import Answer, Category, Question, Quizzes

admin.site.register(Answer)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Quizzes)
