import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório.")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            raise ValueError("A senha é obrigatória.")

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    INDIVIDUAL = 'individual'
    PROFESSIONAL = 'professional'
    COMPANY = 'company'
    
    USER_TYPE_CHOICES = [
        (INDIVIDUAL, 'Cliente'),
        (PROFESSIONAL, 'Profissional'),
        (COMPANY, 'Empresa'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=INDIVIDUAL)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname']

    def __str__(self):
        return self.email
    

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.active = self.end_date > now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Assinatura de {self.user.email} - {'Ativa' if self.active else 'Inativa'}"
    

class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_in_days = models.PositiveIntegerField()

    def __str__(self):
        return self.name


def create_subscription(user, plan):
    end_date = now() + timedelta(days=plan.duration_in_days)
    Subscription.objects.create(user=user, end_date=end_date, active=True)
