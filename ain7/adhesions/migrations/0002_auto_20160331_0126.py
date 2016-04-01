# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 23:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('annuaire', '0002_auto_20160331_0126'),
        ('adhesions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionkey',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annuaire.Person'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='configuration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adhesions.SubscriptionConfiguration', verbose_name='S\xe9lectionnez le tarif applicable'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='last_change_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_changed_subscription', to='annuaire.Person', verbose_name='Auteur de la derni\xe8re modification'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='annuaire.AIn7Member', verbose_name='Saisissez votre nom pour vous identifier'),
        ),
    ]
