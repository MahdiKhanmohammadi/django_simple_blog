from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.crypto import get_random_string

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        get_email = self.normalize_email(email)
        user = self.model(email=get_email, **kwargs)
        user.set_password(password)
        user.save()
        print("user created!")

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)

        return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verify_code = models.CharField(
        max_length=250, unique=True, null=True, blank=True)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        # every time user saved verify code is change
        self.verify_code = get_random_string(22)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "User"
