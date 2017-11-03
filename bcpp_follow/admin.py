from django.contrib import admin

from .admin_site import bcpp_follow_admin
from edc_base.modeladmin_mixins import audit_fieldset_tuple


from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin)
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin

from .forms import WorkListForm
from .models import WorkList


@admin.register(WorkList, site=bcpp_follow_admin)
class WorkListAdmin(ModelAdminNextUrlRedirectMixin,
                    ModelAdminFormInstructionsMixin,
                    ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                    ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                    ModelAdminInstitutionMixin, admin.ModelAdmin):

    form = WorkListForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'map_area',)}),
        audit_fieldset_tuple)

    instructions = ['Complete this form once per day.']
