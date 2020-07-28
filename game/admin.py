from django.contrib import admin
from .models import Question, Quiz, Game, Referral

# Register your models here.
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Game)
admin.site.register(Referral)