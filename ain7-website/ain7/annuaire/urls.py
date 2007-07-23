# -*- coding: utf-8
#
# annuaire/urls.py
#
#   Copyright (C) 2007 AIn7
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

from django.conf.urls.defaults import *

from ain7.annuaire.views import *

urlpatterns = patterns('',

    # Annuaire
    (r'^$', search),
    (r'^(?P<person_id>\d+)/$', detail),
    # Edition
    (r'^(?P<person_id>\d+)/edit/$', edit),
    (r'^(?P<user_id>\d+)/person/edit/$', person_edit),
    (r'^(?P<user_id>\d+)/ain7member/edit/$', ain7member_edit),
    (r'^(?P<user_id>\d+)/avatar/edit/$', avatar_edit),
    # Adresses
    (r'^(?P<user_id>\d+)/address/(?P<address_id>\d+)/edit/$', address_edit),
    (r'^(?P<user_id>\d+)/address/(?P<address_id>\d+)/delete/$', address_delete),
    (r'^(?P<user_id>\d+)/address/add/$', address_add),
    # Phone numbers
    (r'^(?P<user_id>\d+)/phone/(?P<phone_id>\d+)/edit/$', phone_edit),
    (r'^(?P<user_id>\d+)/phone/(?P<phone_id>\d+)/delete/$', phone_delete),
    (r'^(?P<user_id>\d+)/phone/add/$', phone_add),
    # Email
    (r'^(?P<user_id>\d+)/email/(?P<email_id>\d+)/edit/$', email_edit),
    (r'^(?P<user_id>\d+)/email/(?P<email_id>\d+)/delete/$', email_delete),
    (r'^(?P<user_id>\d+)/email/add/$', email_add),
    # Instant messaging
    (r'^(?P<user_id>\d+)/im/(?P<im_id>\d+)/edit/$', im_edit),
    (r'^(?P<user_id>\d+)/im/(?P<im_id>\d+)/delete/$', im_delete),
    (r'^(?P<user_id>\d+)/im/add/$', im_add),
    # Comptes IRC 
    (r'^(?P<user_id>\d+)/irc/(?P<irc_id>\d+)/edit/$', irc_edit),
    (r'^(?P<user_id>\d+)/irc/(?P<irc_id>\d+)/delete/$', irc_delete),
    (r'^(?P<user_id>\d+)/irc/add/$', irc_add),
    # Sites Web 
    (r'^(?P<user_id>\d+)/website/(?P<website_id>\d+)/edit/$', website_edit),
    (r'^(?P<user_id>\d+)/website/(?P<website_id>\d+)/delete/$', website_delete),
    (r'^(?P<user_id>\d+)/website/add/$', website_add),
    # Activités associatives n7
    (r'^(?P<user_id>\d+)/club_membership/(?P<club_membership_id>\d+)/edit/$', club_membership_edit),
    (r'^(?P<user_id>\d+)/club_membership/(?P<club_membership_id>\d+)/delete/$', club_membership_delete),
    (r'^(?P<user_id>\d+)/club_membership/add/$', club_membership_add),

    # Autocompletion
    (r'^complete/track/$', complete_track),
)
