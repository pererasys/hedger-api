'''
Written by Andrew Perera
Copyright 2020
'''


from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from assets.models import Asset
import uuid


class UserAccountManager(BaseUserManager):
    def create_account(self, email, first_name="", last_name="", password=None, is_active=True, is_admin=False, is_staff=False):
        if not email:
            raise ValueError("Users must have an email address.")
        if not password:
            raise ValueError("Users must have a password.")

        account = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        account.set_password(password)
        account.admin = is_admin
        account.staff = is_staff
        account.active = is_active
        account.save(self._db)
        return account

    def create_staffuser(self, username, password=None, is_staff=True):
        account = self.create_account(
            username,
            password=password,
            is_staff=True
        )
        return account

    def create_superuser(self, email, password=None):
        account = self.create_account(
            email=email,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return account


class UserAccount(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    watch_list = models.ManyToManyField(Asset, related_name="watchers", through="WatchedAsset", blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    class Meta:
        verbose_name = 'user account'
        verbose_name_plural = 'user accounts'

    def __str__(self):
        return self.email

    def get_short_name(self):
        if self.first_name != "":
             return self.first_name
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def update_last_login(self):
        self.last_login = now()
        self.save()

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class WatchedAsset(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'watched asset'
        verbose_name_plural = 'watched assets'
        unique_together= ['asset', 'user']
    
    def __str__(self):
        return f'{str(self.user)} is watching {str(self.asset)}.'