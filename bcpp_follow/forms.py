from django import forms

from edc_base.modelform_mixins import JSONModelFormMixin, CommonCleanModelFormMixin
from edc_base.modelform_validators import FormValidatorMixin
from .models import WorkList


class WorkListForm(FormValidatorMixin, CommonCleanModelFormMixin,
                   JSONModelFormMixin, forms.ModelForm):

    class Meta:
        model = WorkList
        fields = '__all__'
