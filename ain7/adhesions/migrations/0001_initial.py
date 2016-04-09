# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 23:26
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_change_at', models.DateTimeField(blank=True, editable=False, verbose_name='Modifi\xe9 pour la derni\xe8re fois \xe0')),
                ('old_id', models.IntegerField(blank=True, null=True, unique=True, verbose_name=b'old id')),
                ('dues_amount', models.FloatField(verbose_name='Montant de cotisation')),
                ('newspaper_amount', models.FloatField(blank=True, null=True, verbose_name='Montant Canal N7')),
                ('tender_type', models.IntegerField(choices=[(1, 'Esp\xe8ce'), (2, 'Ch\xe8que'), (4, 'Carte bancaire'), (5, 'Virement'), (6, 'Autre')], verbose_name='Mode de paiement')),
                ('validated', models.BooleanField(default=False, verbose_name='Valid\xe9')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name="date d'adh\xe9sion")),
                ('start_year', models.IntegerField(verbose_name='d\xe9but (ann\xe9e)')),
                ('end_year', models.IntegerField(verbose_name='fin (ann\xe9e)')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('newspaper_subscription', models.BooleanField(default=False, verbose_name='Adh\xe9rer \xe0 Canal N7 - 15 euros/an')),
                ('user_authenticated', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Adh\xe9sions',
            },
        ),
        migrations.CreateModel(
            name='SubscriptionConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Promotions ant\xe9rieures \xe0 2011'), (1, 'Promotions 2011 \xe0 2015'), (2, 'Retrait\xe9'), (3, 'Bienfaiteur'), (4, 'Sans emploi (sur justificatif)'), (5, '\xc9tudiant(e), trois ans'), (6, '\xc9tudiant(e), deux ans'), (7, '\xc9tudiant(e), un an'), (8, 'Couple'), (9, 'Soutien'), (10, '\xc9tudiant(e)')], verbose_name='Type')),
                ('dues_amount', models.IntegerField(verbose_name='Montant de cotisation')),
                ('newspaper_amount', models.IntegerField(blank=True, null=True, verbose_name='Montant Canal N7')),
                ('duration', models.IntegerField(default=1, verbose_name='Dur\xe9e')),
                ('year', models.IntegerField(verbose_name='Ann\xe9e')),
            ],
            options={
                'verbose_name': 'Configuration',
            },
        ),
        migrations.CreateModel(
            name='SubscriptionKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expire_at', models.DateTimeField(editable=False)),
            ],
        ),
    ]