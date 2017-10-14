from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = 'BCPP Follow'
    site_header = 'BCPP Follow'
    index_title = 'BCPP Follow'
    site_url = '/bcpp_follow/list/'


bcpp_follow_admin = AdminSite(name='bcpp_follow_admin')
