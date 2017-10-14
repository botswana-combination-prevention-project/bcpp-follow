from django.apps import apps as django_apps
from django.db.models.constants import LOOKUP_SEP

from edc_device.constants import CLIENT, SERVER, NODE_SERVER
from edc_map.site_mappers import site_mappers
from edc_map.models import InnerContainer


class MapAreaQuerysetViewMixin:

    subject_queryset_lookups = []

    @property
    def plot_identifiers(self):
        """Returns a list of plot identifiers allocated to this device.
        """
        edc_device_app_config = django_apps.get_app_config('edc_device')
        device_id = edc_device_app_config.device_id
        plot_identifiers = []
        try:
            plot_identifiers = InnerContainer.objects.get(
                device_id=device_id,
                map_area=site_mappers.current_map_area).identifier_labels
        except InnerContainer.DoesNotExist:
            pass
        return plot_identifiers

    @property
    def subject_identifiers(self):
        """Returns a list of subject identifies for an inner container.
        """
        subject_consents = django_apps.get_model(
            'bcpp_subject.subjectconsent').objects.filter(
            household_member__household_structure__household__plot__plot_identifier__in=self.plot_identifiers)
        subject_identifiers = [
            consent.subject_identifier for consent in subject_consents]
        subject_identifiers = list(set(subject_identifiers))
        return subject_identifiers

    def add_dispatched_subject_identifier_filter(self, options=None, **kwargs):
        """Update filter options to limit by dispatched subjects.
        """
        if self.subject_identifiers:
            options.update(
                {'subject_identifier__in': self.subject_identifiers})
        return options

    def add_map_area_filter_options(self, options=None, **kwargs):
        """Updates the filter options to limit the subject returned
        to those in the current map_area.
        """
        options.update(
            {'map_area': site_mappers.current_map_area})
        return options

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        edc_device_app_config = django_apps.get_app_config('edc_device')
        if edc_device_app_config.device_role in [SERVER, CLIENT, NODE_SERVER]:
            options = self.add_map_area_filter_options(
                options=options, **kwargs)
            options = self.add_dispatched_subject_identifier_filter(
                options=options, **kwargs)
        return options
