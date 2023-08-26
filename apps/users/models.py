import datetime

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from store.models import Category


class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    category_id = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    created = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """Create and save a User with the given username and password."""
        if not username:
            raise ValueError('The given phone must be set')
        self.username = username
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        """Create and save a regular User with the given username and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """Create and save a SuperUser with the given username and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    full_name = models.CharField(max_length=150, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # validators should be a list
    phone = models.CharField(validators=[phone_regex], max_length=17)
    city = models.CharField(max_length=50, blank=True, null=True)
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    profile_photo = models.ImageField(default='default.jpg', upload_to='accounts/')
    address_name = models.CharField(max_length=255, null=True, blank=True)
    address_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    address_long = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.full_name

    def get_address(self):
        lat = None
        long = None
        if self.address_lat:
            lat = self.address_lat

        if self.address_long:
            long = self.address_long
        return {
            "name": self.address_name,
            "lat": lat,
            "long": long
        }

    @receiver(post_save, sender=User)  # add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            full_name = ''
            if instance.full_name:
                full_name += instance.full_name

            Profile.objects.create(user=instance, full_name=full_name,
                                   phone_number=instance.phone, address_name=instance.city)

    @receiver(post_save, sender=User)  # add this
    def save_user_profile(sender, instance, **kwargs):
        profile = instance.profile_set.first()
        profile.user = instance
        profile.full_name = instance.full_name
        profile.phone_number = instance.phone
        profile.address_name = instance.city
        profile.save()


class Token(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token', on_delete=models.CASCADE, )
    access = models.CharField(max_length=512, blank=True)
    refresh = models.CharField(max_length=512, blank=True)

    access_expiration = models.DateTimeField(
        default=timezone.now() + datetime.timedelta(minutes=settings.JWT['ACCESS_EXPIRATION_TIME']))
    refresh_expiration = models.DateTimeField(
        default=timezone.now() + datetime.timedelta(days=settings.JWT['REFRESH_EXPIRATION_TIME']))

    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.access:
            self.access = self._generate_access_token

        if not self.refresh:
            self.refresh = self._generate_refresh_token

        return super().save(*args, **kwargs)

    @property
    def _generate_access_token(self):
        access_dt = timezone.now() + \
            datetime.timedelta(minutes=settings.JWT['ACCESS_EXPIRATION_TIME'])
        token = jwt.encode({"token_type": "access", f"{settings.JWT['user']}": self.user.id, "exp": access_dt},
                           settings.SECRET_KEY, algorithm="HS256")
        return token

    @property
    def _generate_refresh_token(self):
        refresh_dt = timezone.now() + \
            datetime.timedelta(minutes=settings.JWT['REFRESH_EXPIRATION_TIME'])
        token = jwt.encode({"token_type": "refresh", f"{settings.JWT['user']}": self.user.id, "exp": refresh_dt},
                           settings.SECRET_KEY, algorithm="HS256")
        return token

    def __str__(self):
        return f'{self.user}'


class EmailRegisterData(models.Model):
    email = models.EmailField(max_length=128)
    code = models.PositiveIntegerField()
    is_used = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
