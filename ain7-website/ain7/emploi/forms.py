# -*- coding: utf-8
#
# emploi/forms.py
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

from django import forms
from django.forms import widgets
from django.forms.util import ValidationError
from django.utils.translation import ugettext as _

from ain7.annuaire.models import Track
from ain7.emploi.models import *
from ain7.fields import AutoCompleteField
from ain7.utils import AIn7Form
from ain7.widgets import DateTimeWidget


dateWidget = DateTimeWidget()
dateWidget.dformat = '%d/%m/%Y'

class JobOfferForm(AIn7Form):
    reference = forms.CharField(label=_('reference').capitalize(), max_length=50,
        required=False, widget=forms.TextInput(attrs={'size':'55'}))
    title = forms.CharField(label=_('title').capitalize(), max_length=50,
        required=True, widget=forms.TextInput(attrs={'size':'55'}))
    experience = forms.CharField(label=_('experience').capitalize(), max_length=50,
        required=False, widget=forms.TextInput(attrs={'size':'55'}))
    contract_type = forms.IntegerField(label=_('contract type'),
        required=False)
    contract_type.widget = forms.Select(choices=JobOffer.JOB_TYPES)
    is_opened = forms.BooleanField(label=_('is opened'),required=False)
    description = forms.CharField(label=_('description').capitalize(),
        required=False,
        widget=forms.widgets.Textarea(attrs={'rows':15, 'cols':80}))
    office = forms.IntegerField(label=_('Office'), required=True,
        widget=AutoCompleteField(completed_obj_name='office'))
    contact_name = forms.CharField(label=_('Contact name'), max_length=50,
        required=False, widget=forms.TextInput(attrs={'size':'55'}))
    contact_email = forms.EmailField(label=_('Contact email').capitalize(),
        required=False)
    activity_field = forms.IntegerField(label=_('Activity field'),
        required=False, widget=AutoCompleteField(completed_obj_name='activity_field'))
    track = forms.ModelMultipleChoiceField(label=_('track').capitalize(),
        queryset=Track.objects.filter(active=True), required=False)
    
    def clean_office(self):
        o = self.cleaned_data['office']
        if o==None:
            raise ValidationError(_('The office is mandatory.'))
            return None
        else:
            office = None
            try:
                office = Office.objects.get(id=o)
            except Office.DoesNotExist:
                raise ValidationError(_('The entered office does not exist.'))
            return office
    
    def clean_activity_field(self):
        a = self.cleaned_data['activity_field']
        if a!=None:
            af = None
            try:
                af = ActivityField.objects.get(pk=a)
            except ActivityField.DoesNotExist:
                raise ValidationError(_('The entered activity field does not exist.'))
            return af
    
    def save(self, user, job_offer=None):
        if not job_offer:
            job_offer = JobOffer()
        job_offer.reference = self.cleaned_data['reference']
        job_offer.title = self.cleaned_data['title']
        job_offer.experience = self.cleaned_data['experience']
        job_offer.contract_type = self.cleaned_data['contract_type']
        job_offer.is_opened = self.cleaned_data['is_opened']
        job_offer.description = self.cleaned_data['description']
        job_offer.office = self.cleaned_data['office']
        job_offer.contact_name = self.cleaned_data['contact_name']
        job_offer.contact_email = self.cleaned_data['contact_email']
        job_offer.activity_field = self.cleaned_data['activity_field']
        job_offer.save()
        # needs to have a primary key before a many-to-many can be used
        job_offer.track = self.cleaned_data['track']
        job_offer.logged_save(user.person)
        return job_offer


class SearchJobForm(forms.Form):
    title = forms.CharField(label=_('title').capitalize(),max_length=50,
        required=False, widget=forms.TextInput(attrs={'size':'40'}))
    allTracks = forms.BooleanField(label=_('all tracks'), required=False)
    track = forms.ModelMultipleChoiceField(label=_('track').capitalize(),
        queryset=Track.objects.all(), required=False)
    activity_field = forms.IntegerField(label=_('Activity field'),
        required=False, widget=AutoCompleteField(completed_obj_name='activity_field'))
    experience = forms.CharField(label=_('experience').capitalize(),
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'size':'40'}))
    contract_type = forms.ChoiceField(label=_('Contract type'),
        required=False, choices=[])

    def __init__(self, *args, **kwargs):
        super(SearchJobForm, self).__init__(*args, **kwargs)
        contract_types = [(0, _('all').capitalize())]
        for i,t in JobOffer.JOB_TYPES:
            contract_types.append((i+1,t))
        self.fields['contract_type'].choices = contract_types

    def clean_contract_type(self):
        return int(self.cleaned_data['contract_type'])

    def search(self):
        # si des filières sont sélectionnées mais pas le joker
        # on filtre par rapport à ces filières
        jobsMatchingTracks = []
        if (not self.cleaned_data['allTracks'])\
               and len(self.cleaned_data['track'])>0:
            for track in self.cleaned_data['track']:
                jobsMatchingTracks.extend(
                    track.jobs.filter(checked_by_secretariat=True))
        else:
            jobsMatchingTracks = JobOffer.objects.filter(
                checked_by_secretariat=True)
        # on filtre par domaine d'activité
        jobsMatchingActivity = []
        if self.cleaned_data['activity_field']:
            for job in jobsMatchingTracks:
                if job.activity_field and \
                    job.activity_field.pk==self.cleaned_data['activity_field']:
                    jobsMatchingActivity.append(job)
        else:
            jobsMatchingActivity = jobsMatchingTracks
        # maintenant on filtre ces jobs par rapport au titre saisi
        matchingJobs = []
        for job in jobsMatchingActivity:
            if str(self.cleaned_data['title']) in job.title and \
                str(self.cleaned_data['experience']) in job.experience and \
                ( self.cleaned_data['contract_type']==0 or
                  self.cleaned_data['contract_type']==job.contract_type+1 ):
                matchingJobs.append(job)
        return matchingJobs

class OrganizationForm(forms.Form):
    name = forms.CharField(
        label=_('Name'), max_length=50, required=True)
    employment_agency = forms.BooleanField(
        label=_('employment agency').capitalize(), required=False)
    size = forms.IntegerField(
        label=_('Size'), required=True,
        widget=forms.Select(choices=Organization.ORGANIZATION_SIZE))
    activity_field = forms.IntegerField(label=_('Activity field'),
        required=False, widget=AutoCompleteField(completed_obj_name='activity_field'))
    short_description = forms.CharField(
        label=_('Short Description'), max_length=50, required=False)
    long_description = forms.CharField(
        label=_('Long Description'), max_length=5000, required=False,
        widget=forms.widgets.Textarea(attrs={'rows':15, 'cols':50}))

    def save(self, user, is_a_proposal=False, organization=None, is_valid=True):
        if organization:
            org = organization
        else:
            org = Organization()
        # TODO : automatiser avec qqchose comme ça:
#         for field in org._meta.fields:
#             if field.name=='is_a_proposal':
#                 field.value = is_a_proposal
#             else:
#                 field.value = self.cleaned_data[field.name]
        org.name = self.cleaned_data['name']
        org.employment_agency = self.cleaned_data['employment_agency']
        org.size = self.cleaned_data['size']
        org.activity_field = ActivityField.objects.get(pk=self.cleaned_data['activity_field'])
        org.short_description = self.cleaned_data['short_description']
        org.long_description = self.cleaned_data['long_description']
        org.is_a_proposal = is_a_proposal
        org.is_valid = is_valid
        org.logged_save(user.person)
        return org

class OfficeForm(forms.ModelForm):
    organization = forms.IntegerField(label=_('Organization'),
        required=True,widget=AutoCompleteField(completed_obj_name='organization'))
    country = forms.ModelChoiceField(
        label=_('country').capitalize(),
        queryset=Country.objects.all(), required=False)

    def clean_organization(self):
        o = self.cleaned_data['organization']
        if o == None:
            raise ValidationError(_('The organization is mandatory.'))
        try:
            o = Organization.objects.get(id=o)
        except Organization.DoesNotExist:
            raise ValidationError(_('The organization does not exist.'))
        else:
            return o
        
    class Meta:
        model = Office
        exclude = ('old_id', 'is_a_proposal', 'is_valid')

class OfficeFormNoOrg(forms.ModelForm):
    country = forms.ModelChoiceField(
        label=_('country').capitalize(),
        queryset=Country.objects.all(), required=False)

    class Meta:
        model = Office
        exclude = ('old_id', 'is_a_proposal', 'is_valid', 'organization')

class PositionForm(forms.ModelForm):
    start_date = forms.DateTimeField(label=_('start date').capitalize(),widget=dateWidget)
    end_date = forms.DateTimeField(label=_('end date').capitalize(), widget=dateWidget, required=False)
    office = forms.IntegerField(label=_('Office'), required=False, widget=AutoCompleteField(completed_obj_name='office'))

    def clean_office(self):
        o = self.cleaned_data['office']

        if o==None:
            raise ValidationError(_('The office is mandatory.'))
        else:
            try:
                office = Office.objects.get(id=self.cleaned_data['office'])
            except Office.DoesNotExist:
                raise ValidationError(_('The entered office does not exist.'))
            return office
    
    class Meta:
        model = Position
        exclude = ('ain7member')

    def clean_end_date(self):
        if self.cleaned_data.get('start_date') and \
            self.cleaned_data.get('end_date') and \
            self.cleaned_data['start_date']>self.cleaned_data['end_date']:
            raise forms.ValidationError(_('Start date is later than end date'))
        return self.cleaned_data['end_date']

class EducationItemForm(forms.ModelForm):
    start_date = forms.DateField(label=_('start year').capitalize(),
        input_formats=['%Y'], widget=forms.DateTimeInput(format='%Y'))
    end_date = forms.DateField(label=_('end year').capitalize(),
        input_formats=['%Y'], widget=forms.DateTimeInput(format='%Y'),
        required=False)
#     diploma = forms.IntegerField(label=_('diploma').capitalize(),
#         widget=AutoCompleteField(completed_obj_name='diploma'), required=False)
    diploma = forms.CharField(label=_('diploma').capitalize(),
        widget=AutoCompleteField(completed_obj_name='diploma'), required=False)

    class Meta:
        model = EducationItem
        exclude = ('ain7member')

    def clean_end_date(self):
        if self.cleaned_data.get('start_date') and \
            self.cleaned_data.get('end_date') and \
            self.cleaned_data['start_date']>self.cleaned_data['end_date']:
            raise forms.ValidationError(_('Start date is later than end date'))
        return self.cleaned_data['end_date']

class LeisureItemForm(forms.ModelForm):
    
    class Meta:
        model = LeisureItem
        exclude = ('ain7member')

class PublicationItemForm(forms.ModelForm):
    date = forms.DateField(label=_('year').capitalize(),
        input_formats=['%Y'], widget=forms.DateTimeInput(format='%Y'))

    class Meta:
        model = PublicationItem
        exclude = ('ain7member')

class ChooseOrganizationForm(forms.Form):
    organization = forms.IntegerField(label=_('Organization'), required=False, widget=AutoCompleteField(completed_obj_name='organization'))

    def clean_organization(self):
        o = self.cleaned_data['organization']

        if o == None:
            raise ValidationError(_('The organization is mandatory.'))

        try:
            Organization.objects.get(id=o)
        except Organization.DoesNotExist:
            raise ValidationError(_('The organization "%s" does not exist.') % o)
        else:
            return self.cleaned_data['organization']

