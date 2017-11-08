from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_call_manager.managers import CallManager, LogManager, LogEntryManager
from edc_call_manager.models import CallModelMixin, LogModelMixin, LogEntryModelMixin


class Call(CallModelMixin, BaseUuidModel):

    call_datetime = models.DateTimeField(
        default=get_utcnow,
        verbose_name='Date of this call')

    objects = CallManager()

    def __str__(self):
        return self.subject_identifier

    @property
    def subject(self):
        return self

    class Meta:
        app_label = 'bcpp_follow'


class Log(LogModelMixin, BaseUuidModel):

    call = models.ForeignKey(Call)

    objects = LogManager()

    class Meta:
        app_label = 'bcpp_follow'


class LogEntry(LogEntryModelMixin, BaseUuidModel):

    log = models.ForeignKey(Log)

    objects = LogEntryManager()

    class Meta:
        app_label = 'bcpp_follow'
