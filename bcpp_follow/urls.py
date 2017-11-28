from django.conf.urls import url
from django.contrib import admin


from .admin_site import bcpp_follow_admin
from .views import ListboardView

app_name = 'bcpp_follow'

admin.autodiscover()

subject_identifier = '066\-[0-9\-]+'

urlpatterns = [
    url(r'^admin/', bcpp_follow_admin.urls),
]


def listboard_urls():
    listboard_configs = [
        ('listboard_url', ListboardView, 'listboard')]

    for listboard_url_name, listboard_view_class, label in listboard_configs:
        urlpatterns.extend([
            url(r'^' + label + '/'
                '(?P<subject_identifier>' + subject_identifier + ')/'
                '(?P<page>\d+)/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/'
                '(?P<subject_identifier>' + subject_identifier + ')/'
                '(?P<page>\d+)/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/'
                '(?P<subject_identifier>' + subject_identifier + ')/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/(?P<page>\d+)/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/',
                listboard_view_class.as_view(), name=listboard_url_name)])
    return urlpatterns

urlpatterns = listboard_urls()
