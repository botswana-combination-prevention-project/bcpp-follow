from django.apps import apps as django_apps

from bcpp_subject.models.subject_consent import SubjectConsent
from edc_model_wrapper.wrappers.model_wrapper import ModelWrapper


class SubjectLocatorModelWrapper(ModelWrapper):
    model_name = 'bcpp_subject.subjectlocator'
    admin_site_name = django_apps.get_app_config(
        'bcpp_subject_dashboard').admin_site_name
    url_namespace = 'bcpp_subject'
    next_url_name = django_apps.get_app_config(
        'bcpp_subject_dashboard').dashboard_url_name
    next_url_attrs = {'bcpp_subject.subjectlocator': [
        'subject_identifier', 'household_identifier',
        'survey_schedule']}
    url_instance_attrs = [
        'subject_identifier', 'household_identifier',
        'survey_schedule']

    @property
    def subject_consent(self):
        return SubjectConsent.objects.filter(
            subject_identifier=self.object.subject_identifier).order_by(
                'consent_datetime').last()

    @property
    def may_follow_up(self):
        return self.object.may_follow_up

    @property
    def first_name(self):
        return self.subject_consent.first_name

    @property
    def last_name(self):
        return self.subject_consent.last_name

    @property
    def contacts(self):
        return ', '.join([
            self.object.subject_cell or '',
            self.object.subject_cell_alt or '',
            self.object.subject_phone or '',
            self.object.subject_phone_alt or ''])

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
