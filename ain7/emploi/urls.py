# -*- coding: utf-8
"""
 ain7/emploi/urls.py
"""
#
#   Copyright © 2007-2016 AIn7 Devel Team
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

from django.conf.urls import url

from ain7.emploi import views


urlpatterns = [
    url(r'^$', views.index, name='job-index'),
    # Job offers
    url(r'^job/add/$', views.job_edit, name='job-add'),
    url(r'^job/(?P<job_id>\d+)/$', views.job_details, name='job-details'),
    url(r'^job/(?P<job_id>\d+)/edit/$', views.job_edit, name='job-edit'),
    url(r'^job/proposals/$', views.jobs_proposals, name='jobs-proposals'),
    url(r'^job/proposals/(?P<job_id>\d+)/validate/$', views.job_validate, name='job-validate'),
    url(r'^job/proposals/(?P<job_id>\d+)/delete/$', views.job_delete, name='job-delete'),
]
