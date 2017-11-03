from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future
from edc_search.model_mixins import SearchSlugModelMixin


class WorkList(SearchSlugModelMixin, BaseUuidModel):

    """A model linked to the subject consent to record corrections.
    """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        unique=True)

    report_datetime = models.DateTimeField(
        verbose_name="Correction report date ad time",
        null=True,
        validators=[
            datetime_not_future],
    )

    map_area = models.CharField(
        max_length=25)

    is_called = models.BooleanField(default=False)

    called_datetime = models.DateTimeField(null=True)

    visited = models.BooleanField(default=False)

    def __str__(self):
        return str(self.subject_identifier,)

    def get_search_slug_fields(self):
        fields = ['subject_identifier']
        return fields

    class Meta:
        app_label = 'bcpp_follow'
