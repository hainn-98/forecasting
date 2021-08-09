from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from .managers import UserManager
from clients.models import Client


class User(AbstractBaseUser, PermissionsMixin, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    USER = 0
    EXPERT = 1
    ADMIN = 2
    USER_TYPE_CHOICES = (
        (USER, 'USER'),
        (EXPERT, 'EXPERT'),
        (ADMIN, 'ADMIN')
    )

    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    role = models.SmallIntegerField(choices=USER_TYPE_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    change_init_password = models.BooleanField(default=False)
    reset_password_token = models.CharField(max_length=255)
    reset_password_token_expired_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, related_name='users', on_delete=models.SET_NULL, unique=False, null=True)

    objects = UserManager()

    class Meta:
        app_label = 'users'
        db_table = 'user'

    @property
    def full_name(self):
        return self.name




