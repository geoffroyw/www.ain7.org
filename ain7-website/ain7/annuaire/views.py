# -*- coding: utf-8
#
# annuaire/views.py
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

import csv
import vobject

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django import newforms as forms

from ain7.annuaire.models import Person, AIn7Member, Address, PhoneNumber
from ain7.annuaire.models import Track, Email, InstantMessaging, IRC, WebSite, ClubMembership
from ain7.annuaire.models import Promo, UserContribution, AIn7Subscription
from ain7.decorators import confirmation_required
from ain7.utils import ain7_render_to_response, ImgUploadForm

class SearchPersonForm(forms.Form):
    last_name = forms.CharField(label=_('Last name'), max_length=50, required=False)
    first_name = forms.CharField(label=_('First name'), max_length=50, required=False)
    promo = forms.IntegerField(label=_('Promo'), required=False)
    track = forms.IntegerField(label=_('Track'), required=False, initial=-1, widget=forms.HiddenInput())

class AdvanceSearchPersonForm(forms.Form):
    last_name = forms.CharField(label=_('Last name'), max_length=50, required=False)
    first_name = forms.CharField(label=_('First name'), max_length=50, required=False)
    promo = forms.IntegerField(label=_('Promo'), required=False)
    track = forms.IntegerField(label=_('Track'), required=False, initial=-1, widget=forms.HiddenInput())
    country = forms.CharField(label=_('Country'), max_length=50, required=False)
    organization = forms.CharField(label=_('Organization'), max_length=50, required=False)
    local_group = forms.CharField(label=_('Local group'), max_length=50, required=False)
    club = forms.CharField(label=_('Club'), max_length=50, required=False)

class SendmailForm(forms.Form):
    subject = forms.CharField(label=_('subject'),max_length=50, required=False, widget=forms.TextInput(attrs={'size':'50'}))
    body = forms.CharField(label=_('body'),max_length=500, required=False, widget=forms.widgets.Textarea(attrs={'rows':15, 'cols':95}))
    send_test = forms.BooleanField(label=_('Send me a test'), required=False)

@login_required
def contributions(request, user_id):
    p = get_object_or_404(Person, pk=user_id)
    ain7member = get_object_or_404(AIn7Member, person=p)
    list_contributions = UserContribution.objects.filter(user=p).order_by('-date')
    return ain7_render_to_response(request, 'annuaire/contributions.html', 
                            {'person': p, 'ain7member': ain7member, 'list_contributions': list_contributions})

@login_required
def details(request, user_id):
    p = get_object_or_404(Person, pk=user_id)
    ain7member = get_object_or_404(AIn7Member, person=p)
    return ain7_render_to_response(request, 'annuaire/details.html', 
                            {'person': p, 'ain7member': ain7member})

@login_required
def search(request):

    f = SearchPersonForm()
    ain7members = False

    if request.method == 'POST':
        form = SearchPersonForm(request.POST)
        if form.is_valid():

            # criteres sur le nom et prenom
            criteria={'person__last_name__contains':form.clean_data['last_name'],\
                      'person__first_name__contains':form.clean_data['first_name']}
            # ici on commence par rechercher toutes les promos
            # qui concordent avec l'annee de promotion et la filiere
            # saisis par l'utilisateur.
            promoCriteria={}
            if form.clean_data['promo'] != None:
                promoCriteria['year']=form.clean_data['promo']
            if form.clean_data['track'] != -1:
                promoCriteria['track']=\
                    Track.objects.get(id=form.clean_data['track'])
                
            # on ajoute ces promos aux critères de recherche
            # si elle ne sont pas vides
            if len(promoCriteria)!=0:
                criteria['promos__in']=Promo.objects.filter(**promoCriteria)

            request.session['filter'] = criteria
                
            ain7members = AIn7Member.objects.filter(**criteria)

    return ain7_render_to_response(request, 'annuaire/search.html', 
                            {'form': f, 'ain7members': ain7members})

@login_required
def advanced_search(request):

    f = AdvanceSearchPersonForm()
    ain7members = False

    if request.method == 'POST':
        form = AdvanceSearchPersonForm(request.POST)
        if form.is_valid():

            # criteres sur le nom et prenom
            criteria={'person__last_name__contains':form.clean_data['last_name'],\
                      'person__first_name__contains':form.clean_data['first_name']}
            # ici on commence par rechercher toutes les promos
            # qui concordent avec l'annee de promotion et la filiere
            # saisis par l'utilisateur.
            promoCriteria={}
            if form.clean_data['promo'] != None:
                promoCriteria['year']=form.clean_data['promo']
            if form.clean_data['track'] != -1:
                promoCriteria['track']=\
                    Track.objects.get(id=form.clean_data['track'])
                
            # on ajoute ces promos aux critères de recherche
            # si elle ne sont pas vides
            if len(promoCriteria)!=0:
                criteria['promos__in']=Promo.objects.filter(**promoCriteria)

            request.session['filter'] = criteria
                
            ain7members = AIn7Member.objects.filter(**criteria)

    return ain7_render_to_response(request, 'annuaire/search.html', 
                            {'form': f, 'ain7members': ain7members})

@login_required
def export_csv(request):

    criteria = request.session['filter']
    ain7members = AIn7Member.objects.filter(**criteria)

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export_ain7.csv'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name'])
    for member in ain7members:
       writer.writerow([member.person.first_name, member.person.last_name])

    return response

@login_required
def sendmail(request):

    criteria = request.session['filter']
    ain7members = AIn7Member.objects.filter(**criteria)

    f= SendmailForm()

    if request.method == 'POST':
        f = SendmailForm(request.POST)
        if f.is_valid():
            if f.clean_data['send_test']:
                request.user.person.send_mail(f.clean_data['subject'],f.clean_data['body'])
            else:
                for member in ain7members:
                    member.person.send_mail(f.clean_data['subject'],f.clean_data['body'])

    return ain7_render_to_response(request, 'annuaire/sendmail.html', 
                            {'form': f})

@login_required
def edit(request, user_id=None):

    p = get_object_or_404(Person, pk=user_id)
    ain7member = get_object_or_404(AIn7Member, person=p)
    return ain7_render_to_response(request, 'annuaire/edit.html',
                            {'person': p, 'ain7member': ain7member})

@login_required
def person_edit(request, user_id=None):

    if user_id is None:
        PersonForm = forms.form_for_model(Person,
            formfield_callback=_form_callback)
        form = PersonForm()

    else:
        person = Person.objects.get(user=user_id)
        PersonForm = forms.form_for_instance(person,
            formfield_callback=_form_callback)
        PersonForm.base_fields['sex'].widget=\
            forms.Select(choices=Person.SEX)
        form = PersonForm(auto_id=False)

        if request.method == 'POST':
             form = PersonForm(request.POST)
             if form.is_valid():
                 form.clean_data['user'] = person.user
                 form.save()
                 request.user.message_set.create(message=_("Modifications have been successfully saved."))
             else:
                 request.user.message_set.create(message=_("Something was wrong in the form you filled. No modification done."))
             return HttpResponseRedirect('/annuaire/%s/edit' % (person.user.id))
    return ain7_render_to_response(request, 'annuaire/edit_form.html', 
                            {'form': form,
                             'action_title': _("Modification of personal data")})

@login_required
def ain7member_edit(request, user_id=None):

    if user_id is None:
        PersonForm = forms.form_for_model(AIn7Member,
            formfield_callback=_form_callback)
        form = PersonForm()

    else:
        person = Person.objects.get(user=user_id)
        ain7member = get_object_or_404(AIn7Member, person=person)
        avatar = ain7member.avatar
        PersonForm = forms.form_for_instance(ain7member,
            formfield_callback=_form_callback)

        if request.method == 'POST':
             post = request.POST.copy()
             post.update(request.FILES)
             form = PersonForm(post)
             if form.is_valid():
                 form.clean_data['person'] = person
                 form.clean_data['avatar'] = avatar
                 form.save()
                 request.user.message_set.create(message=_("Modifications have been successfully saved."))
             else:
                 request.user.message_set.create(message=_("Something was wrong in the form you filled. No modification done."))
             return HttpResponseRedirect('/annuaire/%s/edit' % (person.user.id))
        form = PersonForm(auto_id=False)
    return ain7_render_to_response(request, 'annuaire/edit_form.html', 
                            {'form': form,
                             'action_title':
                             _("Modification of personal data for ") +
                             str(person)})

@login_required
def avatar_edit(request, user_id):

    person = Person.objects.get(user=user_id)
    ain7member = get_object_or_404(AIn7Member, person=person)
    
    if request.method == 'GET':
        form = ImgUploadForm()
        filename = None
        if ain7member.avatar:
            filename = '/site_media/%s' % ain7member.avatar
        return ain7_render_to_response(request, 'pages/image.html',
            {'section': 'annuaire/base.html', 'name': _("avatar").capitalize(),
             'form': form, 'filename': filename})
    else:
        post = request.POST.copy()
        post.update(request.FILES)
        form = ImgUploadForm(post)
        if form.is_valid():
            ain7member.save_avatar_file(
                form.clean_data['img_file']['filename'],
                form.clean_data['img_file']['content'])
            request.user.message_set.create(message=_("The picture has been successfully changed."))
        else:
            request.user.message_set.create(message=_("Something was wrong in the form you filled. No modification done."))
        return HttpResponseRedirect('/annuaire/%s/edit/' % (person.user.id))

@confirmation_required(lambda user_id=None, object_id=None : '', 'annuaire/base.html', _('Do you really want to delete your avatar'))
@login_required
def avatar_delete(request, user_id):

    person = Person.objects.get(user=user_id)
    ain7member = get_object_or_404(AIn7Member, person=person)
    ain7member.avatar = None
    ain7member.save()
    
    request.user.message_set.create(message=
        _('Your avatar has been successfully deleted.'))
    return HttpResponseRedirect('/annuaire/%s/edit/' % user_id)

def _generic_edit(request, user_id, object_id, object_type,
                  person, ain7member, action_title, msg_done):

    obj = get_object_or_404(object_type, pk=object_id)

    # 1er passage : on propose un formulaire avec les donnees actuelles
    if request.method == 'GET':
        PosForm = forms.form_for_instance(obj,
            formfield_callback=_form_callback)
        f = PosForm()
        return ain7_render_to_response(request, 'annuaire/edit_form.html',
                                {'form': f, 'action_title': action_title})
    
    # 2e passage : sauvegarde et redirection
    if request.method == 'POST':
        PosForm = forms.form_for_instance(obj,
            formfield_callback=_form_callback)
        f = PosForm(request.POST.copy())
        if f.is_valid():
            if person is not None:
                f.clean_data['person'] = person
            if ain7member is not None:
                f.clean_data['member'] = ain7member
            f.save()
            request.user.message_set.create(message=msg_done)
        else:
            request.user.message_set.create(message=_("Something was wrong in the form you filled. No modification done."))
        return HttpResponseRedirect('/annuaire/%s/edit/' % user_id)

def _generic_delete(request, user_id, object_id, object_type, msg_done):

    obj = get_object_or_404(object_type, pk=object_id)
    obj.delete()

    request.user.message_set.create(message=msg_done)
    return HttpResponseRedirect('/annuaire/%s/edit/' % user_id)

def _generic_add(request, user_id, object_type, person, ain7member,
                action_title, msg_done):

    # 1er passage : on propose un formulaire vide
    if request.method == 'GET':
        PosForm = forms.form_for_model(object_type,
            formfield_callback=_form_callback)
        f = PosForm()
        return ain7_render_to_response(request, 'annuaire/edit_form.html',
                                {'person': person, 'ain7member': ain7member,
                                 'form': f, 'action_title': action_title})

    # 2e passage : sauvegarde et redirection
    if request.method == 'POST':
        PosForm = forms.form_for_model(object_type,
            formfield_callback=_form_callback)
        f = PosForm(request.POST.copy())
        if f.is_valid():
            if person is not None:
                f.clean_data['person'] = person
            if ain7member is not None:            
                f.clean_data['member'] = ain7member
            f.save()
            request.user.message_set.create(message=msg_done)
        else:
            request.user.message_set.create(message=_('Something was wrong in the form you filled. No modification done.'))
        return HttpResponseRedirect('/annuaire/%s/edit/' % user_id)

# Adresses
@login_required
def address_edit(request, user_id=None, address_id=None):

    return _generic_edit(request, user_id, address_id, Address,
                         get_object_or_404(Person, user=user_id), None,
                         _('Modification of an addressr'),
                         _('Address informations updated successfully.'))

@confirmation_required(lambda user_id=None, address_id=None : str(get_object_or_404(Address, pk=address_id)), 'annuaire/base.html', _('Do you really want to delete your address'))
@login_required
def address_delete(request, user_id=None, address_id=None):

    return _generic_delete(request, user_id, address_id, Address,
                           _('Address successfully deleted.'))

@login_required
def address_add(request, user_id=None):

    return _generic_add(request, user_id, Address,
                        get_object_or_404(Person, user=user_id), None,
                        _('Creation of an address'),
                        _('Address successfully added.'))

# Numeros de telephone
@login_required
def phone_edit(request, user_id=None, phone_id=None):

    return _generic_edit(request, user_id, phone_id, PhoneNumber,
                         get_object_or_404(Person, user=user_id), None,
                         _('Modification of a phone number'),
                         _('Phone number informations updated successfully.'))

@confirmation_required(lambda user_id=None, phone_id=None : str(get_object_or_404(PhoneNumber, pk=phone_id)), 'annuaire/base.html', _('Do you really want to delete your phone number'))
@login_required
def phone_delete(request, user_id=None, phone_id=None):

    return _generic_delete(request, user_id, phone_id, PhoneNumber,
                           _('Phone number successfully deleted.'))

@login_required
def phone_add(request, user_id=None):

    return _generic_add(request, user_id, PhoneNumber,
                        get_object_or_404(Person, user=user_id), None,
                        _('Creation of a phone number'),
                        _('Phone number successfully added.'))

# Adresses de courriel
@login_required
def email_edit(request, user_id=None, email_id=None):

    return _generic_edit(request, user_id, email_id, Email,
                         get_object_or_404(Person, user=user_id), None,
                         _('Modification of an email address'),
                         _('Email informations updated successfully.'))

@confirmation_required(lambda user_id=None, email_id=None : str(get_object_or_404(Email, pk=email_id)), 'annuaire/base.html', _('Do you really want to delete your email address'))
@login_required
def email_delete(request, user_id=None, email_id=None):

    return _generic_delete(request, user_id, email_id, Email,
                           _('Email address successfully deleted.'))

@login_required
def email_add(request, user_id=None):

    return _generic_add(request, user_id, Email,
                        get_object_or_404(Person, user=user_id), None,
                        _('Creation of an email address'),
                        _('Email address successfully added.'))

# Comptes de messagerie instantan�e
@login_required
def im_edit(request, user_id=None, im_id=None):

    return _generic_edit(request, user_id, im_id, InstantMessaging,
                         get_object_or_404(Person, user=user_id), None,
                         _('Modification of an instant messaging account'),
                         _('Instant messaging informations updated successfully.'))

@confirmation_required(lambda user_id=None, im_id=None : str(get_object_or_404(InstantMessaging, pk=im_id)), 'annuaire/base.html', _('Do you really want to delete your instant messaging account'))
@login_required
def im_delete(request, user_id=None, im_id=None):

    return _generic_delete(request, user_id, im_id, InstantMessaging,
                           _('Instant messaging account successfully deleted.'))

@login_required
def im_add(request, user_id=None):

    return _generic_add(request, user_id, InstantMessaging,
                        get_object_or_404(Person, user=user_id), None,
                        _('Creation of an instant messaging account'),
                        _('Instant messaging account successfully added.'))

# Comptes IRC
@login_required
def irc_edit(request, user_id=None, irc_id=None):

    return _generic_edit(request, user_id, irc_id, IRC,
                         get_object_or_404(Person, user=user_id), None,
                         _('Modification of an IRC account'),
                         _('IRC account informations updated successfully.'))

@confirmation_required(lambda user_id=None, irc_id=None : str(get_object_or_404(IRC, pk=irc_id)), 'annuaire/base.html', _('Do you really want to delete your IRC account'))
@login_required
def irc_delete(request, user_id=None, irc_id=None):

    return _generic_delete(request, user_id, irc_id, IRC,
                           _('IRC account successfully deleted.'))

@login_required
def irc_add(request, user_id=None):

    return _generic_add(request, user_id, IRC,
                        get_object_or_404(Person, user=user_id), None,
                        _('Creation of an IRC account'),
                        _('IRC account successfully added.'))

# Sites Internet
@login_required
def website_edit(request, user_id=None, website_id=None):

    return _generic_edit(request, user_id, website_id, WebSite,
                         get_object_or_404(Person, user=user_id), None,
                         _('Modification of a website'),
                         _('Website informations updated successfully.'))

@confirmation_required(lambda user_id=None, website_id=None : str(get_object_or_404(WebSite, pk=website_id)), 'annuaire/base.html', _('Do you really want to delete your website'))
@login_required
def website_delete(request, user_id=None, website_id=None):

    return _generic_delete(request, user_id, website_id, WebSite,
                           _('Website successfully deleted.'))

@login_required
def website_add(request, user_id=None):

    return _generic_add(request, user_id, WebSite,
                        get_object_or_404(Person, user=user_id), None,
                        _('Creation of a website'),
                        _('Website successfully added.'))

# Vie associative a l'n7

@login_required
def club_membership_edit(request, user_id=None, club_membership_id=None):

    person = get_object_or_404(Person, user=user_id)
    return _generic_edit(request, user_id, club_membership_id, ClubMembership,
                         person, get_object_or_404(AIn7Member, person=person),
                         _('Modification of a club membership'),
                         _('Club membership informations updated successfully.'))

@confirmation_required(lambda user_id=None, club_membership_id=None : str(get_object_or_404(ClubMembership, pk=club_membership_id)), 'annuaire/base.html', _('Do you really want to delete your club membership'))
@login_required
def club_membership_delete(request, user_id=None, club_membership_id=None):

    return _generic_delete(request, user_id, club_membership_id, ClubMembership,
                           _('Club membership successfully deleted.'))

@login_required
def club_membership_add(request, user_id=None):

    person = get_object_or_404(Person, user=user_id)
    return _generic_add(request, user_id, ClubMembership,
                        person, get_object_or_404(AIn7Member, person=person),
                        _('Creation of a club membership'),
                        _('Club membership successfully added.'))

@login_required
def subscriptions(request, user_id):

    p = get_object_or_404(Person, pk=user_id)
    ain7member = get_object_or_404(AIn7Member, person=p)

    subscriptions_list = AIn7Subscription.objects.filter(member=ain7member).order_by('-date')

    return ain7_render_to_response(request, 'annuaire/subscriptions.html', 
                            {'person': p, 'ain7member': ain7member, 'subscriptions_list': subscriptions_list})

@login_required
def subscription_edit(request, user_id=None, subscription_id=None):

    return _generic_edit(request, user_id, subscription_id, AIn7Subscription,
                         get_object_or_404(Person, user=user_id), None,
                         _('Modification of a subscription'),
                         _('Subscription informations updated successfully.'))

@confirmation_required(lambda user_id=None, subscription_id=None : str(get_object_or_404(AIn7Subscription, pk=subscription_id)), 'annuaire/base.html', _('Do you really want to delete this subscription'))
@login_required
def subscription_delete(request, user_id=None, subscription_id=None):

    return _generic_delete(request, user_id, subscription_id, AIn7Subscription,
                           _('Subscription successfully deleted.'))

@login_required
def subscription_add(request, user_id=None):

    return _generic_add(request, user_id, AIn7Subscription,
                        get_object_or_404(Person, user=user_id), None,
                        _('Adding a subscription'),
                        _('Subscription successfully added.'))

@login_required
def preferences(request, user_id):

    p = get_object_or_404(Person, pk=user_id)
    ain7member = get_object_or_404(AIn7Member, person=p)

    return ain7_render_to_response(request, 'annuaire/preferences.html', 
                            {'person': p, 'ain7member': ain7member})

@login_required
def vcard(request, user_id):

    p = get_object_or_404(Person, pk=user_id)
    ain7member = get_object_or_404(AIn7Member, person=p)

    mail = None
    mail_list = Email.objects.filter(person=p,preferred_email=True)
    if mail_list:
       mail = mail_list[0].email

    vcard = vobject.vCard()
    vcard.add('n').value = vobject.vcard.Name( family=p.last_name, given=p.first_name )
    vcard.add('fn').value = p.first_name+' '+p.last_name
    if mail:
        vcard.add('mail').value = mail

    vcardstream = vcard.serialize()

    response = HttpResponse(vcardstream, mimetype='text/x-vcard')
    response['Filename'] = p.user.username+'.vcf'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename='+p.user.username+'.vcf'

    return response

# une petite fonction pour exclure certains champs
# des formulaires crees avec form_for_model et form_for_instance
def _form_callback(f, **args):
  exclude_fields = ('person', 'user', 'member', 'avatar')
  if f.name in exclude_fields:
    return None
  return f.formfield(**args)

def complete_track(request):
    elements = []

    if request.method == 'POST':
        input = request.POST['input']
        tracks = Track.objects.filter(name__icontains=input)
        for track in tracks:
            elements.append({'id':track.id, 'value':track.name})

    return ain7_render_to_response(request, 'pages/complete.html', {'elements':elements})

