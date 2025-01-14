from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from users.models import Subscription, User, Plan
from django.utils.timezone import now
from datetime import timedelta


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'name', 'lastname', 'email', 'user_type', 'password', 'password_confirm']
        read_only_fields = ['id']

    def validate(self, attrs):
        # Verifica se as senhas coincidem
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})

        # Verifica se o tipo de usuário é válido
        valid_user_types = [choice[0] for choice in User.USER_TYPE_CHOICES]
        if attrs.get('user_type') not in valid_user_types:
            raise serializers.ValidationError({"user_type": "Tipo de usuário inválido."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'start_date', 'end_date', 'active']
        read_only_fields = ['id', 'active']

    def create(self, validated_data):
        # Garante que uma assinatura válida seja criada
        if validated_data['end_date'] <= validated_data['start_date']:
            raise serializers.ValidationError("A data de término deve ser posterior à data de início.")
        return super().create(validated_data)


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration_in_days']
        read_only_fields = ['id']


class UserWithSubscriptionSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'lastname', 'email', 'user_type', 'subscription']
        read_only_fields = ['id']


class UserWithSubscriptionCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    plan_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'lastname', 'email', 'user_type', 'password', 'password_confirm', 'plan_id']
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})

        if attrs['user_type'] in [User.PROFESSIONAL, User.COMPANY] and not attrs.get('plan_id'):
            raise serializers.ValidationError({"plan_id": "O plano é obrigatório para profissionais e empresas."})

        return attrs

    def create(self, validated_data):
        plan_id = validated_data.pop('plan_id', None)
        validated_data.pop('password_confirm')

        user = User.objects.create_user(**validated_data)

        if plan_id:
            plan = Plan.objects.get(id=plan_id)
            end_date = now() + timedelta(days=plan.duration_in_days)
            Subscription.objects.create(user=user, start_date=now(), end_date=end_date, active=True)

        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Não há nenhum usuário com esse e-mail.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Crie o link de redefinição (ajuste a URL conforme necessário)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        
        # Enviar o e-mail
        send_mail(
            subject="Redefinição de Senha",
            message=f"Use este link para redefinir sua senha: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Link de redefinição inválido.")
        
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Token inválido ou expirado.")
        
        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
