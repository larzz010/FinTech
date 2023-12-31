# Generated by Django 4.2.2 on 2023-06-19 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_name', models.CharField(max_length=100)),
                ('coin_value', models.DecimalField(decimal_places=2, max_digits=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_quantity', models.DecimalField(decimal_places=1, default=0, max_digits=20)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FinApp.coin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FinApp.user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='coins',
            field=models.ManyToManyField(through='FinApp.UserCoin', to='FinApp.coin'),
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FinApp.coin')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Receiver', to='FinApp.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Sender', to='FinApp.user')),
            ],
        ),
        migrations.AddField(
            model_name='coin',
            name='users',
            field=models.ManyToManyField(through='FinApp.UserCoin', to='FinApp.user'),
        ),
    ]
