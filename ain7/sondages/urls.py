# -*- coding: utf-8
"""
 ain7/sondages/urls.py
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


urlpatterns = patterns('ain7.sondages.views',

    # Sondage
    (r'^$', 'index'),
    (r'^(?P<survey_id>\d+)/$', 'view'),
    (r'^(?P<survey_id>\d+)/vote/$', 'vote'),

    # Survey edition
    (r'^add/$', 'edit'),
    (r'^(?P<survey_id>\d+)/details/$', 'details'),
    (r'^(?P<survey_id>\d+)/delete/$', 'delete'),
    (r'^(?P<survey_id>\d+)/edit/$', 'edit'),

    # Choice edition
    (r'^(?P<survey_id>\d+)/choice/add/$', 'choice_edit'),
    (r'^(?P<survey_id>\d+)/choice/(?P<choice_id>\d+)/edit/$', 'choice_edit'),
    (r'^(?P<survey_id>\d+)/choice/(?P<choice_id>\d+)/delete/$', 
        'choice_delete'),

)
