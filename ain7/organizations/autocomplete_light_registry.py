# -*- coding: utf-8
"""
 ain7/annuaire/autocomplete_light_registry.py
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

from autocomplete_light import shortcuts as autocomplete_light

from ain7.organizations.models import (
    Office, Organization, OrganizationActivityField
)


autocomplete_light.register(
    Office,
    search_fields=['name', 'organization__name'],
    add_another_url_name='organization-add',
)
autocomplete_light.register(Organization)
autocomplete_light.register(
    OrganizationActivityField,
    search_fields=['label', 'field'],
    add_another_url_name='organization-activity-add',
)
