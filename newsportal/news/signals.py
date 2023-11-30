from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from news.tasks import post_created_to_task


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if created:
        post_created_to_task.delay(instance.id)

# @receiver(post_save, sender=Post)
# def post_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category=instance.category
#     ).values_list('email', flat=True)
#
#     subject = f'Новый пост в категории {instance.category}'
#
#     text_content = (
#         f'Новость: {instance.title}\n'
#         f'Краткое описание: {instance.content[0:100]}...\n\n'
#         f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Новость: {instance.title}<br>'
#         f'Краткое описание: {instance.content[0:100]}...<br><br>'
#         f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#         f'Ссылка на новость</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
