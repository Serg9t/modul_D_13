from django.contrib import admin

from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'type_category', 'category', 'info')
    list_display_links = ('id', 'title')
    ordering = ('created', 'title')
    list_editable = ('type_category', 'category')
    list_per_page = 5
    actions = ['set_type_news', 'set_type_article']
    search_fields = ['title__startswith', 'category__name']
    list_filter = ['category__name', 'type_category']

    @admin.display(description='Краткое описание')
    def info(self, post: Post):
        return f'Описание {len(post.content)} символов'

    @admin.action(description="Изменить тип на 'Новость'")
    def set_type_news(self, request, queryset):
        count = queryset.update(type_category=Post.Type.NEWS)
        self.message_user(request, f'Изменино {count} записей')

    @admin.action(description="Изменить тип на 'Сатью'")
    def set_type_article(self, request, queryset):
        count = queryset.update(type_category=Post.Type.ARTICLE)
        self.message_user(request, f'Изменино {count} записей')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ('id', 'name')


admin.site.register(Author)
