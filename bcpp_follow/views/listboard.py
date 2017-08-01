import re

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import AppConfigViewMixin
from edc_dashboard.views import ListboardView

from bcpp_subject.models import SubjectLocator

from .wrappers import SubjectLocatorModelWrapper
from edc_map.site_mappers import site_mappers
from edc_device.constants import CLIENT, SERVER


class ListboardView(AppConfigViewMixin, EdcBaseViewMixin, ListboardView):

    model = 'bcpp_subject.subjectlocator'
    model_wrapper_cls = SubjectLocatorModelWrapper
    navbar_item_selected = 'bcpp_follow'
    app_config_name = 'bcpp_follow'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        if kwargs.get('survey_schedule'):
            options.update(
                {'survey_schedule': kwargs.get('survey_schedule')})
        edc_protocol_app_config = django_apps.get_app_config('edc_protocol')
        edc_device_app_config = django_apps.get_app_config('edc_device')
        if edc_device_app_config.device_role in [SERVER, CLIENT]:
            options.update({
                'subject_identifier__startswith': '{}-{}'.format(
                    edc_protocol_app_config.protocol_number,
                    site_mappers.current_map_code)})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
