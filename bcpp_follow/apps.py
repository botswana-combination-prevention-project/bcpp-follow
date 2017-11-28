from django.apps import AppConfig as DjangoAppConfig

from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'bcpp_follow'
    base_template_name = 'edc_base/base.html'
    dashboard_url_name = 'bcpp_follow:listboard_url'
    listboard_url_name = 'bcpp_follow:listboard_url'
    listboard_template_name = 'bcpp_follow/listboard.html'

    def ready(self):
        from bcpp_follow.models import signals


if settings.APP_NAME == 'bcpp_follow':

    from datetime import datetime
    from dateutil.tz import gettz
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_appointment.facility import Facility
    from edc_device.device_permission import DevicePermissions
    from edc_device.device_permission import DeviceAddPermission, DeviceChangePermission
    from edc_device.constants import CENTRAL_SERVER, CLIENT, NODE_SERVER
    from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
    from edc_map.apps import AppConfig as BaseEdcMapAppConfig
    from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig, SubjectType, Cap
    from survey import S
    from survey.apps import AppConfig as BaseSurveyAppConfig
    from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
    from edc_timepoint.timepoint import Timepoint

    class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
        protocol = 'BHP066'
        protocol_number = '066'
        protocol_name = 'BCPP'
        protocol_title = 'Botswana Combination Prevention Project'
        subject_types = [
            SubjectType('subject', 'Research Subject',
                        Cap(model_name='bcpp_subject.subjectconsent', max_subjects=99999)),
            SubjectType('subject', 'Anonymous Research Subject',
                        Cap(model_name='bcpp_subject.anonymousconsent', max_subjects=9999)),
        ]
        study_open_datetime = datetime(
            2013, 10, 18, 0, 0, 0, tzinfo=gettz('UTC'))
        study_close_datetime = datetime(
            2018, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))

        @property
        def site_name(self):
            from edc_map.site_mappers import site_mappers
            return site_mappers.current_map_area

        @property
        def site_code(self):
            from edc_map.site_mappers import site_mappers
            return site_mappers.current_map_code

    class EdcMapAppConfig(BaseEdcMapAppConfig):
        verbose_name = 'Test Mappers'
        mapper_model = 'plot.plot'
        landmark_model = []
        verify_point_on_save = False
        zoom_levels = ['14', '15', '16', '17', '18']
        identifier_field_attr = 'plot_identifier'
        extra_filter_field_attr = 'enrolled'

    class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
        use_settings = True
        device_permissions = DevicePermissions(
            DeviceAddPermission(
                model='plot.plot',
                device_roles=[CENTRAL_SERVER, CLIENT]),
            DeviceChangePermission(
                model='plot.plot',
                device_roles=[NODE_SERVER, CENTRAL_SERVER, CLIENT]))

    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'bcpp_subject': ('subject_visit', 'bcpp_subject.subjectvisit')}

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        app_label = 'bcpp_subject'
        default_appt_type = 'home'
        facilities = {
            'home': Facility(name='home', days=[MO, TU, WE, TH, FR, SA, SU],
                             slots=[99999, 99999, 99999, 99999, 99999, 99999, 99999])}

    class SurveyAppConfig(BaseSurveyAppConfig):

        map_area = settings.CURRENT_MAP_AREA
        current_surveys = [
            S(f'bcpp-survey.bcpp-year-1.bhs.{map_area}'),
            S(f'bcpp-survey.bcpp-year-2.ahs.{map_area}'),
            S(f'bcpp-survey.bcpp-year-3.ahs.{map_area}'),
            S(f'bcpp-survey.bcpp-year-3.ess.{map_area}')]

    class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
        timepoints = [
            Timepoint(
                model='bcpp_subject.appointment',
                datetime_field='appt_datetime',
                status_field='appt_status',
                closed_status='DONE'
            ),
            Timepoint(
                model='bcpp_subject.historicalappointment',
                datetime_field='appt_datetime',
                status_field='appt_status',
                closed_status='DONE'
            ),
        ]