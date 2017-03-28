from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'bcpp_follow'
    base_template_name = 'edc_base/base.html'
    listboard_url_name = 'bcpp_follow:listboard_url'
    listboard_template_name = 'bcpp_follow/listboard.html'
