# Generated by Django 4.2.6 on 2023-10-17 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disc', '0002_pergunta_resposta'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultadoDISC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dominante', models.FloatField(default=0)),
                ('influente', models.FloatField(default=0)),
                ('estabilidade', models.FloatField(default=0)),
                ('conformado', models.FloatField(default=0)),
            ],
        ),
    ]