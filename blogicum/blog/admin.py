from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    list_display = (
        'id',
        'title',
        'is_published',
        'text',
        'author',
        'created_at',
        'pub_date',
    )
    list_display_links = ('id',)
    list_editable = (
        'text',
        'author',
    )
    empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = (
        'id',
        'title',
        'description',
        'slug',
    )
    list_display_links = ('id',)
    list_editable = (
        'title',
        'description',
    )
    empty_value_display = 'Не задано'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = (
        'id',
        'name',
    )
    list_display_links = ('id',)
    list_editable = ('name',)
    empty_value_display = 'Не задано'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    list_display = (
        'id',
        'text',
        'post',
        'created_at',
        'author',
    )
    list_display_links = ('id',)
    list_editable = (
        'text',
        'author',
    )
    empty_value_display = 'Не задано'
