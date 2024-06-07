from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.urls import reverse

from .managers import NewPostManager

User = get_user_model()

PRE_TEXT_LEN: int = 25


class BaseBlogModel(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Category(BaseBlogModel):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=settings.MAXLENGTH,
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL;'
            ' разрешены символы латиницы,'
            ' цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{ self.title[:PRE_TEXT_LEN] }'


class Location(BaseBlogModel):
    name = models.CharField(
        max_length=settings.MAXLENGTH,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return f'{ self.name[:PRE_TEXT_LEN] }'


class Post(BaseBlogModel):

    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем'
                   ' — можно делать отложенные публикации.')
    )
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=settings.MAXLENGTH,
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )

    image = models.ImageField(
        'Изображение',
        upload_to='posts_images',
        blank=True,
    )

    objects = models.Manager()
    custom_manager = NewPostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{ self.title[:PRE_TEXT_LEN] }'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={"post_id": self.pk})


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return '{0} ({1})'.format(self.post, self.author)
