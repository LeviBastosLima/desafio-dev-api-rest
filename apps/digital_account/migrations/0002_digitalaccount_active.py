# Generated by Django 4.0.4 on 2022-04-26 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digital_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='digitalaccount',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
    ]
