import re

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import AppConfigViewMixin
from edc_dashboard.views import ListboardView
from edc_map.site_mappers import site_mappers
from edc_device.constants import CLIENT, SERVER

from ..views.mixins import MapAreaQuerysetViewMixin
from .wrappers import WorkListModelWrapper


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ListboardView(AppConfigViewMixin, EdcBaseViewMixin, MapAreaQuerysetViewMixin, ListboardView):

    model = 'bcpp_follow.worklist'
    model_wrapper_cls = WorkListModelWrapper
    navbar_item_selected = 'bcpp_follow'
    app_config_name = 'bcpp_follow'
    listboard_url_name = django_apps.get_app_config(
        'bcpp_follow').listboard_url_name

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            total_results=self.get_queryset().count(),
            called_subject=len(
                [obj for obj in self.get_queryset() if obj.is_called]),
            visited_subjects=len(
                [obj for obj in self.get_queryset() if obj.visited]),
        )
        return context
