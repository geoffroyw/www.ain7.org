# -*- coding: utf-8
#
# groupes_regionaux/urls.py
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

urlpatterns = patterns('',

    # Groupes Regionaux
    (r'^$', 'ain7.groupes_regionaux.views.index'),
    (r'^(?P<group_id>\d+)/$', 'ain7.groupes_regionaux.views.details'),
    (r'^(?P<group_id>\d+)/edit/$', 'ain7.groupes_regionaux.views.edit'),
    (r'^(?P<group_id>\d+)/join/$', 'ain7.groupes_regionaux.views.join'),
    (r'^(?P<group_id>\d+)/quit/$', 'ain7.groupes_regionaux.views.quit'),

)
