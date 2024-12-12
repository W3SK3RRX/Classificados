# Generated by Django 5.1.3 on 2024-12-10 18:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rua', models.CharField(max_length=255)),
                ('numero', models.CharField(max_length=10)),
                ('complemento', models.CharField(blank=True, max_length=255, null=True)),
                ('bairro', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=2)),
                ('cep', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='PerfilProfissional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('profissional', 'Profissional Liberal'), ('empresa', 'Empresa')], max_length=15)),
                ('foto_logo', models.ImageField(blank=True, null=True, upload_to='uploads/fotos_perfil/')),
                ('profile_name', models.CharField(default='', max_length=40)),
                ('cpf', models.CharField(blank=True, max_length=14, null=True)),
                ('cnpj', models.CharField(blank=True, max_length=18, null=True)),
                ('telefone', models.CharField(max_length=15)),
                ('area_atuacao', models.CharField(max_length=200)),
                ('biografia', models.TextField(blank=True, null=True)),
                ('certificados', models.FileField(blank=True, null=True, upload_to='uploads/certificados/')),
                ('registros_profissionais', models.FileField(blank=True, null=True, upload_to='uploads/registros_profissionais/')),
                ('concordou_termos', models.BooleanField(default=True)),
                ('endereco', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_profissional', to='perfil_profissional.endereco')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
