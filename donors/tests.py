from datetime import date, timedelta
from django.test import TestCase

from donors.compatibility import (
    compatible_donor_groups, filter_available_donors,
    is_universal_donor, is_universal_recipient,
)
from donors.validators import validate_phone, validate_email, validate_blood_group
from donors.exceptions import (
    InvalidPhoneError, InvalidEmailError, InvalidBloodGroupError, CampDateError,
)
from donors.core import Donor, BloodRequest, MatchEngine
from donors.exceptions import NoMatchingDonorError
from donors.datetime_utils import parse_camp_date, is_camp_upcoming, days_until_camp


class CompatibilityTests(TestCase):

    def test_ab_positive_is_universal_recipient(self):
        self.assertTrue(is_universal_recipient('AB+'))
        self.assertEqual(len(compatible_donor_groups('AB+')), 8)

    def test_o_negative_is_universal_donor(self):
        self.assertTrue(is_universal_donor('O-'))
        
        self.assertEqual(compatible_donor_groups('O-'), ['O-'])

    def test_unknown_blood_group_raises(self):
        with self.assertRaises(ValueError):
            compatible_donor_groups('XYZ')

    def test_filter_available_donors_respects_availability_and_location(self):
        pool = [
            {'name': 'A', 'blood_group': 'O-', 'location': 'Nagpur', 'available': True},
            {'name': 'B', 'blood_group': 'O-', 'location': 'Nagpur', 'available': False},
            {'name': 'C', 'blood_group': 'O-', 'location': 'Mumbai', 'available': True},
            {'name': 'D', 'blood_group': 'A+', 'location': 'Nagpur', 'available': True},
        ]
        
        matches = filter_available_donors(pool, 'AB+', location='Nagpur')
        names = {m['name'] for m in matches}
        self.assertEqual(names, {'A', 'D'})


class ValidatorTests(TestCase):

    def test_valid_indian_phone_passes(self):
        self.assertEqual(validate_phone('9876543210'), '9876543210')
        self.assertEqual(validate_phone('+919876543210'), '+919876543210')

    def test_invalid_phone_raises(self):
        with self.assertRaises(InvalidPhoneError):
            validate_phone('12345')
        with self.assertRaises(InvalidPhoneError):
            validate_phone('5876543210')

    def test_valid_email_passes(self):
        self.assertEqual(validate_email('Ravi@Example.com'), 'ravi@example.com')

    def test_invalid_email_raises(self):
        with self.assertRaises(InvalidEmailError):
            validate_email('not-an-email')

    def test_valid_blood_group_passes(self):
        for g in ['A+', 'a-', 'AB+', 'o-']:
            validate_blood_group(g)

    def test_invalid_blood_group_raises(self):
        with self.assertRaises(InvalidBloodGroupError):
            validate_blood_group('C+')
        with self.assertRaises(InvalidBloodGroupError):
            validate_blood_group('A')


class CoreOOPTests(TestCase):

    def test_donor_construction_validates_fields(self):
        d = Donor("Asha", "o+", "9876543210", "Asha@Mail.com", "Nagpur")
        self.assertEqual(d.blood_group, 'O+')
        self.assertEqual(d.email, 'asha@mail.com')

    def test_donor_construction_rejects_bad_phone(self):
        with self.assertRaises(InvalidPhoneError):
            Donor("Asha", "O+", "123", "asha@mail.com", "Nagpur")

    def test_match_engine_finds_compatible_donor_same_location(self):
        donors = [
            Donor("Asha", "O+", "9876543210", "asha@mail.com", "Nagpur"),
            Donor("Vijay", "A+", "9123456780", "vijay@mail.com", "Nagpur"),
            Donor("Ravi", "O+", "9988776655", "ravi@mail.com", "Mumbai"),
        ]
        req = BloodRequest("City Hospital", "O+", "Nagpur", units_needed=1)
        engine = MatchEngine(donors)
        matches = engine.find_matches(req, same_location_only=True)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['name'], 'Asha')

    def test_match_engine_raises_when_no_compatible_donor(self):
        donors = [Donor("Vijay", "A+", "9123456780", "vijay@mail.com", "Nagpur")]
        req = BloodRequest("City Hospital", "O-", "Nagpur", units_needed=1)
        engine = MatchEngine(donors)
        with self.assertRaises(NoMatchingDonorError):
            engine.find_matches(req)

    def test_best_match_prefers_exact_blood_group(self):
        donors = [
            Donor("Vijay", "O-", "9123456780", "vijay@mail.com", "Nagpur"),
            Donor("Asha", "AB+", "9876543210", "asha@mail.com", "Nagpur"),
        ]
        req = BloodRequest("City Hospital", "AB+", "Nagpur", units_needed=1)
        engine = MatchEngine(donors)
        best = engine.best_match(req)
        self.assertEqual(best['blood_group'], 'AB+')


class DateTimeUtilTests(TestCase):

    def test_parse_valid_future_date(self):
        future = (date.today() + timedelta(days=10)).isoformat()
        parsed = parse_camp_date(future)
        self.assertEqual(parsed.isoformat(), future)

    def test_parse_past_date_raises(self):
        past = (date.today() - timedelta(days=1)).isoformat()
        with self.assertRaises(CampDateError):
            parse_camp_date(past)

    def test_parse_bad_format_raises(self):
        with self.assertRaises(CampDateError):
            parse_camp_date('10th August')

    def test_is_camp_upcoming(self):
        near = date.today() + timedelta(days=5)
        far = date.today() + timedelta(days=100)
        self.assertTrue(is_camp_upcoming(near, within_days=30))
        self.assertFalse(is_camp_upcoming(far, within_days=30))