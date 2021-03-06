# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 23:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('annuaire', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_change_at', models.DateTimeField(blank=True, editable=False, verbose_name='Modifi\xe9 pour la derni\xe8re fois \xe0')),
                ('slug', models.CharField(max_length=50, unique=True, verbose_name='slug')),
                ('name', models.CharField(max_length=100, verbose_name='nom')),
                ('about', models.TextField(blank=True, null=True, verbose_name='description')),
                ('is_active', models.BooleanField(default=True, verbose_name='actif')),
                ('private', models.BooleanField(default=False)),
                ('web_site', models.URLField(blank=True, max_length=50, null=True, verbose_name='site internet')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='courriel')),
                ('icon', models.ImageField(blank=True, null=True, upload_to=b'data/', verbose_name='ic\xf4ne')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='GroupAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_change_at', models.DateTimeField(blank=True, editable=False, verbose_name='Modifi\xe9 pour la derni\xe8re fois \xe0')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('last_change_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_changed_groupaccess', to='annuaire.Person', verbose_name='Auteur de la derni\xe8re modification')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nom')),
                ('access', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.GroupAccess')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='groups.Group', verbose_name='groupe')),
            ],
        ),
        migrations.CreateModel(
            name='GroupLeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date de d\xe9but')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Date de fin')),
                ('board_member', models.BooleanField(default=False)),
                ('rank', models.IntegerField(blank=True, null=True, verbose_name='rang')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='titre')),
                ('grouphead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.GroupHead', verbose_name="Conseil d'administration")),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='council_roles', to='annuaire.Person', verbose_name='membre')),
            ],
        ),
        migrations.CreateModel(
            name='GroupRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nom')),
                ('rank', models.IntegerField(verbose_name='rang par d\xe9faut')),
            ],
        ),
        migrations.CreateModel(
            name='GroupType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_change_at', models.DateTimeField(blank=True, editable=False, verbose_name='Modifi\xe9 pour la derni\xe8re fois \xe0')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('group_name_prefix', models.CharField(blank=True, max_length=20, null=True)),
                ('access', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.GroupAccess')),
                ('last_change_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_changed_grouptype', to='annuaire.Person', verbose_name='Auteur de la derni\xe8re modification')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_change_at', models.DateTimeField(blank=True, editable=False, verbose_name='Modifi\xe9 pour la derni\xe8re fois \xe0')),
                ('is_administrator', models.BooleanField(default=False)),
                ('start_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date de d\xe9but')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Date de fin')),
                ('expiration_date', models.DateField(blank=True, null=True, verbose_name="Date d'expiration")),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='groups.Group', verbose_name='groupe')),
                ('last_change_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_changed_member', to='annuaire.Person', verbose_name='Auteur de la derni\xe8re modification')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='annuaire.Person', verbose_name='membre')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='groupleader',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.GroupRole', verbose_name='r\xf4le'),
        ),
        migrations.AddField(
            model_name='group',
            name='access',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.GroupAccess'),
        ),
        migrations.AddField(
            model_name='group',
            name='last_change_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_changed_group', to='annuaire.Person', verbose_name='Auteur de la derni\xe8re modification'),
        ),
        migrations.AddField(
            model_name='group',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.GroupType'),
        ),
    ]
