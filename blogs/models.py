from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

    def all(self):
        return super().all()


class Post(models.Model):
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    objects = models.Manager()
    published = PublishedManager()

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blogs_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT)

    def get_absolute_url(self):
        return reverse("blogs:post_detail",
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])

    def __str__(self):
        return self.title
