from django.apps import apps as django_apps
from django.conf import settings
from django.core.management.base import BaseCommand

from bcpp_follow.models import WorkList


def to_string(value):
    """Returns a string.

    Converts UUID to string using .hex.
    """
    try:
        value = str(value.hex)
    except AttributeError:
        pass
    return value


class Command(BaseCommand):

    help = 'Update registration identifiers.'

    def add_arguments(self, parser):
        parser.add_argument('map_area', type=str, help='map_area')

    def handle(self, *args, **options):
        map_area = options['map_area']
        try:
            inner_container = django_apps.get_model(
                'edc_map.innercontainer').objects.get(
                    map_area=map_area,
                    device_id=settings.DEVICE_ID)
        except django_apps.get_model('edc_map.innercontainer').DoesNotExist:
            subject_visits = django_apps.get_model(
                'bcpp_subject.subjectvisit').objects.filter(
                    household_member__household_structure__household__plot__map_area=map_area,
                    visit_code__in=['T0', 'T1'])
        else:
            subject_visits = django_apps.get_model(
                'bcpp_subject.subjectvisit').objects.filter(
                    household_member__household_structure__household__plot__map_area=map_area,
                    visit_code__in=['T0', 'T1'],
                    household_member__household_structure__household__plot__plot_identifier__in=inner_container.identifier_labels)
        count = 0
        total_participants = len(
            list(set([visit.subject_identifier for visit in subject_visits])))
        for subject_visit in subject_visits:
            try:
                WorkList.objects.get(
                    subject_identifier=subject_visit.subject_identifier)
            except WorkList.DoesNotExist:
                WorkList.objects.create(
                    subject_identifier=subject_visit.subject_identifier,
                    map_area=subject_visit.household_member.household_structure.household.plot.map_area)
                count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'{count} of {total_participants} work list populated.'))
        self.stdout.write(
            self.style.SUCCESS('Successfully populated the work list.'))
