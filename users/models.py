from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Введите почту')
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='Телефон', help_text='Введите телефон')
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name='Город', help_text='Укажите город')
    avatar = models.ImageField(upload_to='users/avatar', null=True, blank=True, verbose_name='Аватар', help_text='Укажите аватар')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
