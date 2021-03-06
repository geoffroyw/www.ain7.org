# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 23:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manage', '0001_initial'),
        ('annuaire', '0002_auto_20160331_0126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=200, null=True, verbose_name='Description')),
                ('option', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ArticlePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Article')),
                ('filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage.Filter')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='PackageCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=200, null=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='montant')),
                ('type', models.IntegerField(choices=[(1, 'Esp\xe8ce'), (2, 'Ch\xe8que CE'), (3, 'Ch\xe8que CCP'), (4, 'Carte bancaire'), (5, 'Virement CE'), (6, 'Virement CCP'), (7, 'Autre')], verbose_name='Type')),
                ('bank', models.CharField(blank=True, max_length=200, null=True, verbose_name='Banque')),
                ('check_number', models.CharField(blank=True, max_length=200, null=True, verbose_name='Num\xe9ro de ch\xe8que')),
                ('date', models.DateField(null=True, verbose_name='Date de paiement')),
                ('validated', models.BooleanField(default=False, verbose_name='Valid\xe9')),
                ('deposited', models.DateTimeField(blank=True, null=True, verbose_name='date de d\xe9p\xf4t')),
                ('created_at', models.DateTimeField(editable=False, verbose_name="Date d'enregistrement")),
                ('modified_at', models.DateTimeField(editable=False, verbose_name='date de modification')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_added', to='annuaire.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='nom')),
                ('public', models.BooleanField(default=False, verbose_name='public')),
                ('obsolete', models.BooleanField(default=False, verbose_name='obsolete')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('saved', models.BooleanField(default=False)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annuaire.Person')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Package')),
                ('shoppingcart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ShoppingCart')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='payment',
            name='modified_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_modified', to='annuaire.Person'),
        ),
        migrations.AddField(
            model_name='payment',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='annuaire.Person'),
        ),
        migrations.AddField(
            model_name='package',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.PackageCategory'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annuaire.Person'),
        ),
        migrations.AddField(
            model_name='order',
            name='shoppingcart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ShoppingCart'),
        ),
        migrations.AddField(
            model_name='article',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Package'),
        ),
    ]
