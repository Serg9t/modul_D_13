from django.db import models
from django.db.models import Sum
from django.urls import reverse

from django.core.cache import cache

from django.utils import timezone

from django.contrib.auth.models import User


class TypeNewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type_category=Post.Type.NEWS)


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rat = self.post_set.aggregate(postRating=Sum('rating'))
        p_rat = 0
        p_rat += post_rat.get('postRating')

        comment_rat = self.author_user.comment_set.aggregate(commentRating=Sum('rating'))
        c_rat = 0
        c_rat += comment_rat.get('commentRating')

        self.author_rating = p_rat * 3 + c_rat
        self.save()

    def __str__(self):
        return self.author_user.username


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    DoesNotExist = None

    # NEWS = 'NW'
    # ARTICLE = 'AR'
    # CATEGORY_CHOICES = [
    #     (NEWS, 'Новость'),
    #     (ARTICLE, 'Статья'),
    # ]

    class Type(models.TextChoices):
        NEWS = 'NW', 'Новость'
        ARTICLE = 'AR', 'Статья'

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    type_category = models.CharField(max_length=2, choices=Type.choices, default=Type.ARTICLE, verbose_name='Тип')
    content = models.TextField(verbose_name='Текст')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Новости и статьи'
        verbose_name_plural = 'Новости и статьи'
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'news_id': self.pk})

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[0:123] + '...'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


# class PostCategory(models.Model):
#     post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
#     category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return self.category.name
