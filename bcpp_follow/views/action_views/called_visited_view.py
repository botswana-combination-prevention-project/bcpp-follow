from django.apps import apps as django_apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from edc_base.utils import get_utcnow

from .base_action_view import BaseActionView
from bcpp_follow.models import WorkList


app_config = django_apps.get_app_config('bcpp_follow')


class CalledVisitedView(BaseActionView):

    post_url_name = app_config.listboard_url_name
    valid_form_actions = ['called', 'visited']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def called_form_action(self):
        if not self.selected_items:
            message = ('Nothing to do. No items selected.')
            messages.warning(self.request, message)
        if self.action == 'called':
            self.called()
        elif self.action == 'visited':
            self.visited()

    def called(self):
        """Updates selected work list to called.
        """
        updated = WorkList.objects.filter(
            pk__in=self.worklist).exclude(
                is_called=True).update(
                    is_called=True, called_datetime=get_utcnow())
        if updated:
            message = ('{} participants called.'.format(updated))
            messages.success(self.request, message)
        return updated

    def visited(self):
        """Updates selected work list to visited.
        """
        updated = WorkList.objects.filter(
            pk__in=self.worklist).exclude(
                visited=True).update(
                    visited=True)
        if updated:
            message = ('{} participants visited.'.format(updated))
            messages.success(self.request, message)
        return updated

    @property
    def worklist(self):
        return self.selected_items
