from django.apps import apps as django_apps
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
        subject_consents = django_apps.get_model(
            'bcpp_subject.subjectconsent').objects.filter(
                household_member__household_structure__household__plot__map_area=map_area)
        count = 0
        total_consents = subject_consents.count()
        for subject_consent in subject_consents:
            try:
                WorkList.objects.get(
                    subject_identifier=subject_consent.subject_identifier)
            except WorkList.DoesNotExist:
                WorkList.objects.create(
                    subject_identifier=subject_consent.subject_identifier,
                    map_area=subject_consent.household_member.household_structure.household.plot.map_area)
                count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'{count} of {total_consents} work list populated.'))
        self.stdout.write(
            self.style.SUCCESS('Successfully populated the work list.'))
