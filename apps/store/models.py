from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.ImageField(upload_to='icons/', null=True)

    def __str__(self):
        return self.name

    def get_post_count(self):
        total = 0
        if self.children:
            for child in self.children.all():
                total+=child.post_set.all().count()
        return total


class Post(models.Model):
    CURRENCY_CHOICES = [
        ('1', 'UZS'),
        ('2', 'USD'),
    ]

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    published_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    phone_number = models.CharField(max_length=20)
    seller = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PostImage(models.Model):
    post = models.ForeignKey(
        Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')

    def __str__(self):
        return str(self.post)
