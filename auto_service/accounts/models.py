from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'CLIENT', _('Клієнт')
        MANAGER = 'MANAGER', _('Менеджер')
        MECHANIC = 'MECHANIC', _('Механік')
        ADMIN = 'ADMIN', _('Адміністратор')

    email = models.EmailField(_('Email'), unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
        verbose_name=_('Роль')
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Телефон'))
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_('Аватар'))
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    class Meta:
        verbose_name = _('Користувач')
        verbose_name_plural = _('Користувачі')
