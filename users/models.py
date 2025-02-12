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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Retorna o nome completo do usuário."""
        return f"{self.name} {self.lastname}".strip()
    

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    active = models.BooleanField(default=False)
    payment_confirmed = models.BooleanField(default=False)  # Novo campo para confirmar o pagamento

    def save(self, *args, **kwargs):
        # A assinatura só é ativa se o pagamento for confirmado e a data de término for no futuro
        if self.payment_confirmed and self.end_date > now():
            self.active = True
        else:
            self.active = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Assinatura de {self.user.email} - {'Ativa' if self.active else 'Inativa'}"

    

class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_in_days = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)  # Campo para descrição do plano

    def __str__(self):
        return self.name


def create_subscription(user, plan):
    end_date = now() + timedelta(days=plan.duration_in_days)
    Subscription.objects.create(user=user, end_date=end_date, active=True)
