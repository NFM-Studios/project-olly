from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('private', 'Private'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE, blank=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='news_images', blank=True)

    # default manager
    objects = models.Manager()

    # specific manager
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.slug


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


@receiver(models.signals.post_delete, sender=Post)
# This should never be run in theory. It would only be hit if the Post was completely deleted
def auto_delete_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete()


@receiver(models.signals.pre_save, sender=Post)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Post.objects.get(pk=instance.pk).image
    except Post.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        old_file.delete(save=False)
