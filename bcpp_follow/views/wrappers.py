from django.apps import apps as django_apps
from edc_base.utils import age, get_utcnow
from edc_model_wrapper import ModelWrapper
from edc_call_manager.models import Call, Log, LogEntry


class WorkListModelWrapper(ModelWrapper):

    model = 'bcpp_follow.worklist'
    next_url_name = django_apps.get_app_config(
        'bcpp_follow').dashboard_url_name
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier']

    @property
    def subject_locator(self):
        SubjectLocator = django_apps.get_model('bcpp_subject.subjectlocator')
        try:
            return SubjectLocator.objects.get(
                subject_identifier=self.object.subject_identifier)
        except SubjectLocator.DoesNotExist:
            return None

    @property
    def call_datetime(self):
        return self.object.called_datetime

    @property
    def call(self):
        call = Call.objects.filter(
            subject_identifier=self.object.subject_identifier).order_by('scheduled').last()
        return str(call.id)

    @property
    def call_log(self):
        call = Call.objects.filter(
            subject_identifier=self.object.subject_identifier).order_by('scheduled').last()
        call_log = Log.objects.get(call=call)
        return str(call_log.id)

    @property
    def log_entries(self):
        call = Call.objects.filter(
            subject_identifier=self.object.subject_identifier).order_by('scheduled').last()
        return LogEntry.objects.filter(
            log__call__subject_identifier=call.subject_identifier).order_by('call_datetime')[:3]

    @property
    def subject_consent(self):
        return django_apps.get_model(
            'bcpp_subject.subjectconsent').objects.filter(
            subject_identifier=self.object.subject_identifier).last()

    @property
    def may_follow_up(self):
        if self.subject_locator:
            return self.subject_locator.may_follow_up
        return None

    @property
    def age_in_years(self):
        return age(self.subject_consent.dob, get_utcnow()).years

    @property
    def map_area(self):
        return self.subject_consent.household_member.household_structure.household.plot.map_area

    @property
    def first_name(self):
        return self.subject_consent.first_name

    @property
    def last_name(self):
        return self.subject_consent.last_name

    @property
    def contacts(self):
        if self.subject_locator:
            return ', '.join([
                self.subject_locator.subject_cell or '',
                self.subject_locator.subject_cell_alt or '',
                self.subject_locator.subject_phone or '',
                self.subject_locator.subject_phone_alt or ''])
        return None

    @property
    def household_identifier(self):
        return (self.subject_consent
                .household_member
                .household_structure
                .household
                .household_identifier)

    @property
    def survey_schedule(self):
        return (self.subject_consent.household_member.survey_schedule)
