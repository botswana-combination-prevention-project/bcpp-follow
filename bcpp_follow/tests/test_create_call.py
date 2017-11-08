from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.test import TestCase

from faker import Faker
from model_mommy import mommy

from bcpp_subject.models import SubjectConsent, SubjectLocator
from bcpp_subject.tests.test_mixins import SubjectMixin
from edc_base.utils import get_utcnow
from edc_consent.site_consents import site_consents
from edc_constants.constants import NO, YES
from edc_registration.models import RegisteredSubject
from household.constants import ELIGIBLE_REPRESENTATIVE_PRESENT
from household.tests.household_test_helper import HouseholdTestHelper
from member.tests.member_test_helper import MemberTestHelper
from survey.site_surveys import site_surveys
from survey.tests.survey_test_helper import SurveyTestHelper

from .worklist_test_helper import WorkListTestHelper
from ..models import Call


fake = Faker()


class TestSubjectConsent(SubjectMixin, TestCase):

    member_helper = MemberTestHelper()
    survey_helper = SurveyTestHelper()
    household_helper = HouseholdTestHelper()
    worklist_test_helper = WorkListTestHelper()

    def setUp(self):
        django_apps.app_configs['edc_device'].device_id = '99'
        self.survey_schedule_object = site_surveys.get_survey_schedules()[0]
        self.household_structure = self.member_helper.make_household_ready_for_enumeration(
            make_hoh=False,
            report_datetime=self.survey_schedule_object.start)

        household_status = ELIGIBLE_REPRESENTATIVE_PRESENT

        mommy.make_recipe(
            'household.householdlogentry',
            report_datetime=get_utcnow(),
            household_log=self.household_structure.householdlog,
            household_status=household_status)

        # add another member, OK!
        household_member = self.member_helper.add_household_member(
            self.household_structure, relation='Mother')
        enrollment_checklist = mommy.make_recipe(
            'member.enrollmentchecklist',
            household_member=household_member,
            report_datetime=self.household_structure.report_datetime,
            dob=(self.household_structure.report_datetime -
                 relativedelta(years=household_member.age_in_years)).date(),
            gender=household_member.gender,
            initials=household_member.initials,
        )

        # fake values
        fake_identity = fake.credit_card_number()
        last_name = fake.last_name().upper()
        initials = enrollment_checklist.initials
        last_name = initials[1] + last_name
        options = {'identity': '317115159', 'confirm_identity': '317115159', }

        try:
            registered_subject = RegisteredSubject.objects.get(
                registration_identifier=household_member.internal_identifier)
        except RegisteredSubject.DoesNotExist:
            identity = options.get('identity', fake_identity)
            confirm_identity = options.get('confirm_identity', fake_identity)
            dob = options.get('dob', enrollment_checklist.dob)
        else:
            identity = options.get('identity', registered_subject.identity)
            confirm_identity = options.get(
                'confirm_identity', registered_subject.identity)
            dob = registered_subject.dob

        self.report_datetime = self.get_utcnow()
        consent_object = site_consents.get_consent(
            report_datetime=self.report_datetime,
            consent_model='bcpp_subject.subjectconsent')

        consent_options = dict(
            first_name=household_member.first_name,
            last_name=last_name,
            consent_datetime=self.report_datetime,
            version=consent_object.version,
            dob=dob,
            gender=options.get('gender', enrollment_checklist.gender),
            initials=initials,
            is_literate=options.get(
                'is_literate', enrollment_checklist.literacy),
            witness_name=options.get(
                'witness_name',
                fake.last_name() if enrollment_checklist.literacy == NO else None),
            legal_marriage=options.get(
                'legal_marriage', enrollment_checklist.legal_marriage),
            marriage_certificate=options.get(
                'marriage_certificate',
                enrollment_checklist.marriage_certificate),
            guardian_name=options.get(
                'guardian_name',
                fake.name() if enrollment_checklist.guardian == YES else None),
            identity=identity,
            confirm_identity=confirm_identity)

        # add subject consent
        self.subject_consent = SubjectConsent.objects.create(
            household_member=household_member,
            survey_schedule=household_member.survey_schedule_object.field_value,
            **consent_options)
        SubjectLocator.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=self.report_datetime,
            alt_contact_cell_number='72200111',
            has_alt_contact=NO,
            alt_contact_name=None,
            alt_contact_rel=None,
            alt_contact_cell=None,
            other_alt_contact_cell='760000111',
            alt_contact_tel=None)

    def test_create_call(self):
        """Test if a call is created if a worklist is created.
        """
        options = dict(
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=self.report_datetime,
            map_area='test_community')
        self.worklist_test_helper.make_worklist(**options)
        self.assertEqual(Call.objects.all().count(), 1)
