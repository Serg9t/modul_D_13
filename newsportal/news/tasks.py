import datetime
from celery import shared_task

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from .models import Post, Subscription


@shared_task
def post_created_to_task(post_id):
    post = Post.objects.get(id=post_id)

    emails = User.objects.filter(subscriptions__category=post.category).values_list('email', flat=True)

    subject = f'Новый пост в категории {post.category}'

    text_content = (
        f'Новость: {post.title}\n'
        f'Краткое описание: {post.content[0:100]}...\n\n'
        f'Ссылка на новость: http://127.0.0.1:8000{post.get_absolute_url()}'
    )
    html_content = (
        f'Новость: {post.title}<br>'
        f'Краткое описание: {post.content[0:100]}...<br><br>'
        f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
        f'Ссылка на новость</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def week_new_post():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(created__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Subscription.objects.filter(category__name__in=categories).values_list('user__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

