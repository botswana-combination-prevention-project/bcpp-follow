import re

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import AppConfigViewMixin
from edc_dashboard.views import ListboardView

from bcpp_subject.models import SubjectLocator

from .wrappers import SubjectLocatorModelWrapper
from edc_map.site_mappers import site_mappers


class ListboardView(AppConfigViewMixin, EdcBaseViewMixin, ListboardView):

    model = SubjectLocator
    model_wrapper_class = SubjectLocatorModelWrapper
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
        options.update({
            'subject_identifier__startswith': '066-{}'.format(site_mappers.current_map_code)})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
