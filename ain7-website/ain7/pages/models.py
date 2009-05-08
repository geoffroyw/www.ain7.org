# -*- coding: utf-8
#
# pages/models.py
#
#   Copyright © 2007-2009 AIn7 Devel Team
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

from django.db import models
from django.utils.translation import ugettext as _

from ain7.utils import LoggedClass


class Text(LoggedClass):

    shortname = models.CharField(verbose_name=_('shortname'), max_length=50)
    title = models.CharField(verbose_name=_('title'), max_length=150)
    body = models.TextField(verbose_name=_('body'), blank=True, null=True)

