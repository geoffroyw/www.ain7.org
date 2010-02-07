# -*- coding: utf-8
"""
 ain7/annuaire/urls.py
"""
#
#   Copyright © 2007-2010 AIn7 Devel Team
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#

from django.conf.urls.defaults import patterns

urlpatterns = patterns('ain7.annuaire.views',
    # Annuaire
    (r'^$', 'search'),
    (r'^csv/$', 'export_csv'),
    (r'^add/$', 'add'),
    (r'^(?P<user_id>\d+)/$', 'details'),
    # Advanced search
    (r'^advanced_search/$', 'advanced_search'),
    (r'^advanced_search/csv/$', 'adv_export_csv'),
    (r'^advanced_search/filter/new/$', 'filter_new'),
    (r'^advanced_search/filter/register/$', 'filter_register'),
    (r'^advanced_search/filter/(?P<filter_id>\d+)/$', 'filter_details'),
    (r'^advanced_search/filter/(?P<filter_id>\d+)/edit/$', 'filter_edit'),
    (r'^advanced_search/filter/(?P<filter_id>\d+)/reset/$', 'filter_reset'),
    (r'^advanced_search/filter/(?P<filter_id>\d+)/delete/$', 'filter_delete'),
    (r'^advanced_search/filter/(?P<filter_id>\d*)/swapOp/$', 'filter_swap_op'),
    (r'^advanced_search/filter/(?P<filter_id>\d*)/criterion/add/$',
     'criterion_add'),
    (r'^advanced_search/filter/(?P<filter_id>\d*)/criterion/add/field/$',
     'criterion_add', {'criterion_type': 'field'}),
    (r'^advanced_search/filter/(?P<filter_id>\d*)/criterion/add/filter/$',
     'criterion_add', {'criterion_type': 'filter'}),
    (r'^advanced_search/filter/(?P<filter_id>\d+)/criterion/edit/field/$',
     'criterionField_edit'),
    (r'^advanced_search/filter/(?P<filter_id>\d+)/criterion/edit/filter/$',
     'criterionFilter_edit'),
    (r'^advanced_search/filter/(?P<filter_id>\d+)/criterion/(?P<criterion_id>\
\d+)/edit/field/$',
     'criterionField_edit'),
    (r'^advanced_search/filter/(?P<filter_id>\d+)/criterion/(?P<criterion_id>\
\d+)/edit/filter/$',
     'criterionFilter_edit'),
    (r'^advanced_search/filter/(?P<filtr_id>\d+)/criterion/(?P<crit_id>\d+)\
/delete/field/$',
     'criterion_delete', {'crit_type': 'field'}),
    (r'^advanced_search/filter/(?P<filtr_id>\d+)/criterion/(?P<crit_id>\d+)\
/delete/filter/$',
     'criterion_delete', {'crit_type': 'filter'}),
    # Edition
    (r'^(?P<user_id>\d+)/edit/$', 'edit'),
    (r'^(?P<user_id>\d+)/credentials/$', 'change_credentials'),
    (r'^(?P<user_id>\d+)/sendcredentials/$', 'send_new_credentials'),
    (r'^(?P<user_id>\d+)/person/edit/$', 'person_edit'),
    (r'^(?P<user_id>\d+)/personprivate/edit/$', 'personprivate_edit'),
    (r'^(?P<user_id>\d+)/ain7member/edit/$', 'ain7member_edit'),
    (r'^(?P<user_id>\d+)/avatar/delete/$', 'avatar_delete'),
    # Promos
    (r'^(?P<person_id>\d+)/promo/(?P<promo_id>\d+)/delete/$', 'promo_delete'),
    (r'^(?P<person_id>\d+)/promo/add/$', 'promo_edit'),
    # Adresses
    (r'^(?P<user_id>\d+)/address/(?P<address_id>\d+)/edit/$', 'address_edit'),
    (r'^(?P<user_id>\d+)/address/(?P<address_id>\d+)/delete/$',
        'address_delete'),
    (r'^(?P<user_id>\d+)/address/add/$', 'address_edit'),
    # Phone numbers
    (r'^(?P<user_id>\d+)/phone/(?P<phone_id>\d+)/edit/$', 'phone_edit'),
    (r'^(?P<user_id>\d+)/phone/(?P<phone_id>\d+)/delete/$', 'phone_delete'),
    (r'^(?P<user_id>\d+)/phone/add/$', 'phone_edit'),
    # Email
    (r'^(?P<user_id>\d+)/email/(?P<email_id>\d+)/edit/$', 'email_edit'),
    (r'^(?P<user_id>\d+)/email/(?P<email_id>\d+)/delete/$', 'email_delete'),
    (r'^(?P<user_id>\d+)/email/add/$', 'email_edit'),
    # Instant messaging
    (r'^(?P<user_id>\d+)/im/(?P<im_id>\d+)/edit/$', 'im_edit'),
    (r'^(?P<user_id>\d+)/im/(?P<im_id>\d+)/delete/$', 'im_delete'),
    (r'^(?P<user_id>\d+)/im/add/$', 'im_edit'),
    # Comptes IRC
    (r'^(?P<user_id>\d+)/irc/(?P<irc_id>\d+)/edit/$', 'irc_edit'),
    (r'^(?P<user_id>\d+)/irc/(?P<irc_id>\d+)/delete/$', 'irc_delete'),
    (r'^(?P<user_id>\d+)/irc/add/$', 'irc_edit'),
    # Sites Web
    (r'^(?P<user_id>\d+)/website/(?P<website_id>\d+)/edit/$', 'website_edit'),
    (r'^(?P<user_id>\d+)/website/(?P<website_id>\d+)/delete/$',
        'website_delete'),
    (r'^(?P<user_id>\d+)/website/add/$', 'website_edit'),
    # Activités associatives n7
    (r'^(?P<user_id>\d+)/club_membership/(?P<club_membership_id>\d+)/edit/$',
        'club_membership_edit'),
    (r'^(?P<user_id>\d+)/club_membership/(?P<club_membership_id>\d+)/delete/$',
        'club_membership_delete'),
    (r'^(?P<user_id>\d+)/club_membership/add/$', 'club_membership_edit'),
    # vCard
    (r'^(?P<user_id>\d+)/vcard/$', 'vcard'),

)