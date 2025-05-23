# Generated by Django 5.2 on 2025-04-11 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('data_nascimento', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Loja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('endereco', models.CharField(max_length=255)),
                ('estado', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unidade', models.CharField(max_length=3)),
                ('qtd_estoque', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UnidadeMedida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=3, unique=True)),
                ('descricao', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_venda', models.DateField()),
                ('quantidade', models.IntegerField()),
                ('valor_venda', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vendedor', models.CharField(max_length=50)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.cliente')),
                ('loja', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.loja')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.produto')),
            ],
        ),
    ]
