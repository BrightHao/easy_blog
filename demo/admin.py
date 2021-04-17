from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Article)
admin.site.register(models.ArticleClassification)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.Mood)
