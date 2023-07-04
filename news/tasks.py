import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Post, Category


@shared_task
def notify_about_new_post(instance_id):
    instance = Post.objects.get(pk=instance_id)
    categories = instance.postCategory.all()
    subscribers = []

    for category in categories:
        subscribers += category.subscribers.all()

    subscribers = list(set(s.email for s in subscribers))
    print(subscribers)

    for mail in subscribers:
        html_content = render_to_string(
            'post_created_email.html',
            {'text': instance.preview, 'link': f'{settings.SITE_URL}/posts/{instance_id}'}
        )
        msg = EmailMultiAlternatives(
            subject=instance.title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[mail],
            )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task()
def weekly_notifications():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Posts for the week',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
