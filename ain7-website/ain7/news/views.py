# -*- coding: utf-8
#
# news/views.py
#
#   Copyright (C) 2007-2008 AIn7
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

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import ObjectPaginator, InvalidPage
from django import newforms as forms
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext as _

from ain7.news.models import *
from ain7.news.forms import *
from ain7.utils import ain7_render_to_response, ain7_generic_edit, ain7_generic_delete
from ain7.decorators import confirmation_required


def index(request):
    news = NewsItem.objects.all().order_by('-creation_date')[:20]
    return ain7_render_to_response(request, 'news/index.html', {'news': news })

def details(request, news_id):
    news_item = get_object_or_404(NewsItem, pk=news_id)
    return ain7_render_to_response(request, 'news/details.html',
                            {'news_item': news_item})

@login_required
def edit(request, news_id):

    news_item = get_object_or_404(NewsItem, pk=news_id)
    return ain7_generic_edit(
        request, news_item, NewsForm, {}, 'news/edit.html',
        {'news_item':news_item}, {}, '/actualites/%s/' % (news_id),
        _('News successfully updated.'))

@confirmation_required(lambda news_id=None, object_id=None : '', 'base.html', _('Do you really want to delete the image of this news'))
@login_required
def image_delete(request, news_id):

    news_item = get_object_or_404(NewsItem, pk=news_id)
    news_item.image = None
    news_item.save()

    request.user.message_set.create(message=
        _('The image of this news item has been successfully deleted.'))
    return HttpResponseRedirect('/actualites/%s/edit/' % news_id)

@login_required
def add(request):

    return ain7_generic_edit(
        request, None, NewsForm, {}, 'news/write.html',
        {}, {}, '/actualites/', _('News successfully added.'))

def search(request):

    form = SearchNewsForm()
    nb_results_by_page = 25
    list_news = False
    paginator = ObjectPaginator(NewsItem.objects.none(),nb_results_by_page)
    page = 1

    if request.method == 'POST':
        form = SearchNewsForm(request.POST)
        if form.is_valid():
            list_news = form.search()
            paginator = ObjectPaginator(list_news,nb_results_by_page)

            try:
                page = int(request.GET.get('page', '1'))
                list_news = paginator.get_page(page - 1)

            except InvalidPage:
                raise http.Http404

    return ain7_render_to_response(request, 'news/search.html',
        {'form': form, 'list_news': list_news,
         'request': request,'paginator': paginator,
         'is_paginated': paginator.pages > 1,
         'has_next': paginator.has_next_page(page - 1),
         'has_previous': paginator.has_previous_page(page - 1),
         'current_page': page,
         'next_page': page + 1, 'previous_page': page - 1,
         'pages': paginator.pages,
         'first_result': (page - 1) * nb_results_by_page +1,
         'last_result': min((page) * nb_results_by_page, paginator.hits),
         'hits' : paginator.hits,})
