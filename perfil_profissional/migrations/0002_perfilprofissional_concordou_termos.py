# Generated by Django 5.1.3 on 2024-12-02 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil_profissional', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilprofissional',
            name='concordou_termos',
            field=models.BooleanField(default=False),
        ),
    ]
